var cc = DataStudioApp.createCommunityConnector();

function getAuthType() {
  var AuthTypes = cc.AuthType;
  return cc
    .newAuthTypeResponse()
    .setAuthType(AuthTypes.NONE)
    .build();
}

function getConfig(request) {
  var config = cc.getConfig();
  
  config.newInfo()
    .setId('instructions')
    .setText('Select a country to view their data.');
  
  config.newSelectSingle()
    .setId('country')
    .setName('Select a country')
    .addOption(config.newOptionBuilder().setLabel('Singapore').setValue('singapore'))
    .addOption(config.newOptionBuilder().setLabel('Malaysia').setValue('malaysia'));
  
  config.setDateRangeRequired(true);
  
  return config.build();
}

function getFields(request) {
  var cc = DataStudioApp.createCommunityConnector();
  var fields = cc.getFields();
  var types = cc.FieldType;
  
  fields.newDimension()
    .setId('country')
    .setType(types.TEXT);

  fields.newMetric()
    .setId('confirmed')
    .setType(types.NUMBER);
  
  fields.newMetric()
    .setId('deaths')
    .setType(types.NUMBER);
  
  fields.newMetric()
    .setId('recovered')
    .setType(types.NUMBER);

  fields.newDimension()
    .setId('date')
    .setType(types.YEAR_MONTH_DAY_SECOND);
  
  return fields;
}

function getSchema(request) {
  var fields = getFields(request).build();
  return { schema: fields };
}

function responseToRows(requestedFields, response) {
  // Transform parsed data and filter for requested fields
  return response.map(function(data) {
    var row = [];
    requestedFields.asArray().forEach(function (field) {
      switch (field.getId()) {
        case 'country':
          return row.push(data.Country);
        case 'confirmed':
          return row.push(data.Confirmed);
        case 'deaths':
          return row.push(data.Deaths);
        case 'recovered':
          return row.push(data.Recovered);
        case 'date':
          return row.push(data.Date.replace(/[ZT:-]/g, ''));
        default:
          return row.push('');
      }
    });
    return { values: row };
  });
}

function getData(request) {
  var requestedFieldIds = request.fields.map(function(field) {
    return field.name;
  });
  var requestedFields = getFields().forIds(requestedFieldIds);

  // Fetch and parse data from API
  var url = [
    'https://api.covid19api.com/total/country/',
    request.configParams.country,
    '?from=',
    request.dateRange.startDate,
    '&to=',
    request.dateRange.endDate
  ];
  var response = UrlFetchApp.fetch(url.join(''));
  var parsedResponse = JSON.parse(response);
  var rows = responseToRows(requestedFields, parsedResponse);

  return {
    schema: requestedFields.build(),
    rows: rows
  };
}

/*
var request = {
  dateRange: {
    startDate: '2022-01-01',
    endDate: '2022-02-01'
  },
  configParams: {
    country : 'singapore'
  },
  scriptParams: {
  },
  fields: [
    {name: 'country'},
    {name: 'confirmed'},
    {name: 'deaths'},
    {name: 'recovered'},
    {name: 'date'}
  ]
}

Logger.log(getData(request));
*/