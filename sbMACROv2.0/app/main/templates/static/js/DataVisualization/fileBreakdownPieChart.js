var height
var width
function getPieChartSize() {
  width = window.innerWidth * 0.25
  height = width
  let chartSize = {
    width: width,
    height: height,
    radius: Math.min(width, height) / 2,
    donutWidth: width * 0.2,
    legendRectSize: width * 0.05,
    legendSpacing: width * 0.01
  }
  return chartSize
}

// See following for foundational code:
// http://zeroviscosity.com/d3-js-step-by-step/step-1-a-basic-pie-chart
function createPieChart(d3, project, modalId) {
  'use strict'
  let dataset = project.file_breakdown
  let chartSize = getPieChartSize()

  let color = d3.scaleOrdinal(d3.schemeCategory10)

  let svg = d3
    .select('#' + modalId + ' #modal_chart')
    .append('svg')
    .attr('width', chartSize.width)
    .attr('height', chartSize.height)
    .append('g')
    .attr(
      'transform',
      'translate(' + chartSize.width / 2 + ',' + chartSize.height / 2 + ')'
    )

  if (dataset.length == 0) {
    svg
      .append('text')
      .attr('y', 0.1 * height)
      .attr('x', width / 2)
      .attr('dy', '1em')
      .attr('font-size', '1.2em')
      .attr('font-style', 'italic')
      .style('fill', 'grey')
      .style('text-anchor', 'middle')
      .text('No Files Found')
    return
  }

  let arc = d3
    .arc()
    .innerRadius(chartSize.radius - chartSize.donutWidth)
    .outerRadius(chartSize.radius)

  let pie = d3
    .pie()
    .value(function(d) {
      return d.count
    })
    .sort(null)

  let tooltip = d3
    .select('#' + modalId + ' #modal_chart')
    .append('div')
    .attr('class', 'tooltip')
  tooltip.append('div').attr('class', 'label')
  tooltip.append('div').attr('class', 'count')
  tooltip.append('div').attr('class', 'percent')

  dataset.forEach(function(d) {
    d.enabled = true
  })

  let path = svg
    .selectAll('path')
    .data(pie(dataset))
    .enter()
    .append('path')
    .attr('d', arc)
    .attr('id', function(d, i) {
      return (
        'pieChart-' +
        d.data.label.replace('application/', '').replace('image/', '')
      )
    })
    .attr('fill', function(d, i) {
      return color(d.data.label)
    }) // UPDATED (removed semicolon)
    .each(function(d) {
      this._current = d
    })
  path.on('mouseover', function(d) {
    let total = d3.sum(
      dataset.map(function(d) {
        return d.enabled ? d.count : 0 // UPDATED
      })
    )
    let percent = Math.round((1000 * d.data.count) / total) / 10
    tooltip.select('.label').html('<strong>Type: </strong>' + d.data.label)
    tooltip.select('.count').html('<strong>Count: </strong>' + d.data.count)
    tooltip
      .select('.percent')
      .html('<strong>Percentage of Total: </strong>' + percent + '%')
    tooltip.style('display', 'block')
  })
  path.on('mouseout', function() {
    tooltip.style('display', 'none')
  })
  //OPTIONAL
  path.on('mousemove', function(d) {
    tooltip
      .style('top', d3.event.layerY + 10 + 'px')
      .style('left', d3.event.layerX + 10 + 'px')
  })

  let legend = svg
    .selectAll('.legend')
    .data(color.domain())
    .enter()
    .append('g')
    .attr('class', 'legend')
    .attr('transform', function(d, i) {
      let height = chartSize.legendRectSize + chartSize.legendSpacing
      let offset = (height * color.domain().length) / 2
      let horz = -2 * chartSize.legendRectSize
      let vert = i * height - offset
      return 'translate(' + horz + ',' + vert + ')'
    })
  legend
    .append('rect')
    .attr('width', chartSize.legendRectSize)
    .attr('height', chartSize.legendRectSize)
    .style('fill', color)
    .style('stroke', color) // UPDATED (removed semicolon)
    .on('click', function(label) {
      let rect = d3.select(this)
      let enabled = true
      let totalEnabled = d3.sum(
        dataset.map(function(d) {
          return d.enabled ? 1 : 0
        })
      )
      if (rect.attr('class') === 'disabled') {
        rect.attr('class', '')
      } else {
        if (totalEnabled < 2) return
        rect.attr('class', 'disabled')
        enabled = false
      }
      pie.value(function(d) {
        if (d.label === label) d.enabled = enabled
        return d.enabled ? d.count : 0
      })
      path = path.data(pie(dataset))
      path
        .transition()
        .duration(750)
        .attrTween('d', function(d) {
          let interpolate = d3.interpolate(this._current, d)
          this._current = interpolate(0)
          return function(t) {
            return arc(interpolate(t))
          }
        })
    })
  legend
    .append('text')
    .attr('x', chartSize.legendRectSize + chartSize.legendSpacing)
    .attr('y', chartSize.legendRectSize - chartSize.legendSpacing)
    .text(function(d) {
      return d.replace('application/', '').replace('image/', '')
    })
}
window.d3
