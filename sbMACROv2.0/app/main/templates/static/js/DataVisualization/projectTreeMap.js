function projectTreeMap(projectArray) {
  let data = projectArray
  console.log(data)
  var n = 0
  for (i = 0; i < projectArray.length; i++) {
    if (projectArray[i].num_of_files > 0) {
      n = projectArray[i].num_of_files
    }
  }
  console.log(n)
  if (n <= 0) {
    let d = data
    console.log(d[0].casc)
    var margin = {
      top: 40,
      right: 20,
      bottom: 30,
      left: 60
    },
      width = 960 - margin.left - margin.right,
      height = 150 - margin.top - margin.bottom
    //Should set width and height dynamically
    updateFYDimensions(window.innerWidth, window.innerHeight)
    //Come back to this to change graph layout for small screen sizes
    var breakPoint = 768
    // set the ranges
    var y = d3.scaleLinear().range([0, height])

    var x = d3.scaleLinear().range([0, width])

    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3
      .select('svg g')
      .append('g')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

    // Scale the range of the data in the domains
    x.domain([0, 100])
    // y.domain(d3.range(data.length));
    y.domain([0, 100])
    //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

    //Adding x axis label
    svg
      .append('text')
      .attr('class', 'svg')
      .attr('y', 0.1 * height)
      .attr('x', width / 2)
      .attr('dy', '1em')
      .attr('font-size', '20px')
      .attr('font-style', 'italic')
      .style('fill', 'grey')
      .style('text-anchor', 'middle')
      .text('Selected ' + d[0].casc + ' Projects')

    svg
      .append('text')
      .attr('y', 0.3 * height)
      .attr('x', width / 2)
      .attr('class', 'svg')
      .attr('dy', '1em')
      .attr('font-size', '20px')
      .attr('font-style', 'italic')
      .style('fill', 'grey')
      .style('text-anchor', 'middle')
      .text('contain no data')

    //Updating dimensions
    function updateFYDimensions(winWidth, winHeight) {
      margin.top = 40
      margin.right = winWidth < breakPoint ? 0 : 20
      margin.left = winWidth < breakPoint ? 0 : 50
      margin.bottom = 30

      width = winWidth * 0.5 - margin.left - margin.right
      height = winHeight * 0.25
    }
  }
  var nest = d3.nest().key(function (d) { return d.casc; })
    .key(function (d) { return d.fiscal_year; })
    .key(function (d) { return Number(d.num_of_files != 0); })
    .sortValues(function (a, b) { return Number(b.num_of_files) - Number(a.num_of_files); })

  //console.log(nest)

  var color = d3.scaleOrdinal(d3.schemeCategory10);

  var rootNode = d3.hierarchy({ values: nest.entries(data) }, function (d) { if (d.key != 0) { return d.values; } })
    .sort((a, b) => b.value - a.value);
  console.log(rootNode)
  var margin = {
    top: 40,
    right: 20,
    bottom: 30,
    left: 60
  },
    width = 960 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom
  //Should set width and height dynamically
  updateFYDimensions(window.innerWidth, window.innerHeight)
  //Come back to this to change graph layout for small screen sizes
  var breakPoint = 768

  var treemapLayout = d3.treemap()
    .size([1200, 1200])
    .paddingOuter(5);
  console.log(rootNode)
  //var rootNode = d3.hierarchy(data)
  rootNode.sum(function (d) {

    return Number(d.data_in_project_GB);

  });

  treemapLayout(rootNode);



  var nodes = d3.select('svg g')
    .selectAll('g')
    .data(rootNode.descendants())
    .enter()
    .append('g')
    .attr('transform', function (d) { return 'translate(' + [d.x0, d.y0] + ')' })

  var tool_tip = d3
    .tip()
    .attr('class', 'd3-tip')
    .offset([0, 0])
    .html(function (d) {
      var rStr = d.data.data_in_project_GB + "".toString().substring(0, 4)
      var rFY = d.data.fiscal_year
      var rCSC = d.data.casc
      if (parseFloat(rStr) < 0.01) {
        rStr = 'Less than 0.01'
      } else {
        rStr = '~' + rStr
      }
      return (
        'Science Center: ' +
        rCSC +
        '<br>' +
        '<br>' +
        'Fiscal Year: ' +
        rFY +
        '<br>' +
        '<br>' +
        'Project Number: ' +
        d.data.id +
        '<br>' +
        '<br>' +
        rStr +
        'gb' +
        '<br>' +
        '<br>' +
        'Number of files: ' +
        d.data.num_of_files
      )
    })
  nodes.call(tool_tip)
  nodes
    .append('rect')
    .attr('class', 'node')
    .attr('width', function (d) { return d.x1 - d.x0; })
    .attr('height', function (d) { return d.y1 - d.y0; })
    .style("fill", function (d) { return d.value ? color(d.data.casc) : null; })
    .style('color', 'orange')
    .on('click', function (d) {
      let id
      if (d.data.Number>2 ) {
        let num = d.data.Number + 2
        id = 'p' + num
      } else {
        id = 'table_head'
      }

      document.getElementById(id).scrollIntoView()
    })
    .on('mouseover', tool_tip.show)
    .on('mouseout', tool_tip.hide)
  // nodes
  //   .append('text')
  //   .attr('dx', 2)
  //   .attr('dy', 14)
  //   .text(function (d) {
  //     if (d.data.casc) {
  //       d.data.casc = d.data.casc.split(' ')
  //       d.data.casc = d.data.casc[0];
  //     }
  //     return (d.data.casc);
  //   })
  nodes.forEach(function(d) { d.y = d.depth * 180; }); 
  // nodes
  //   .append('text')
  //   .attr('dx', 2)
  //   .attr('dy', 28)
  //   .text(function (d) {
  //     if (d.data.fiscal_year) {
  //       d.data.fiscal_year = d.data.fiscal_year.replace('FY ', 'FY:')
  //     }
  //     return (d.data.fiscal_year);
  //   })
  // nodes
  //   .append('text')
  //   .attr('dx', 2)
  //   .attr('dy', 40)
  //   .text(function (d) {
  //     if (d.data.id) {
  //       d.data.id = 'Pno:' + (d.data.id)
  //     }
  //     return (d.data.id);
  //   })
  // nodes
  //   .append('text')
  //   .attr('dx', 2)
  //   .attr('dy', 55)
  //   .text(function (d) {
  //     if (d.data.num_of_files) {
  //       d.data.num_of_files = d.data.num_of_files + 'files'
  //     }
  //     return (d.data.num_of_files);
  //   })

  function updateFYDimensions(winWidth, winHeight) {
    margin.top = 40
    margin.right = winWidth < breakPoint ? 0 : 20
    margin.left = winWidth < breakPoint ? 0 : 50
    margin.bottom = 30

    width = winWidth * 0.5 - margin.left - margin.right
    height = winHeight * 0.25
  }
}
