var values = rfc_list;  // set in the loaded .json script

function formatCount(d) {
  if (d==0) { return ""; }
  return d;
}

// http://stackoverflow.com/questions/2752349/fast-rectangle-to-rectangle-intersection
function intersect(a, b) {
  return (a.left <= b.right &&
          b.left <= a.right &&
          a.top <= b.bottom &&
          b.top <= a.bottom)
}

function urlFromRFCNumber(number) {
  return 'http://tools.ietf.org/html/' + number;
}

function fractionOfTotalLinesForSectionTitle(entry, section_title) {
  if (entry["sections"] && entry["sections"][section_title]) {
    return entry["sections"][section_title]/entry["lines"];
  }
  return 0;
}

function pointGraphsForSection(data_list, insertion_selector, section_title, label) {
  var filtered_list = data_list;
  // var filtered_list = data_list.filter(function(el){
  //   if(el["sections"] && el["sections"][section_title]) {
  //     return el;
  //   }
  // });
  
  var x = d3.time.scale().domain(d3.extent(filtered_list, function(d) {return new Date(d["date_published"]);})).nice(d3.time.year).range([0, width]);
  var y = d3.scale.linear() // although some details are easier to see with a log scale
  .domain([0,d3.max(filtered_list, function(d) {
      if (d["sections"]) {
        return d["sections"][section_title];
      } else {
        return 0;
      }
    })])
    .range([height, 0]);
  
  var color = d3.scale.linear().domain([0,d3.max(filtered_list, function(d) { return fractionOfTotalLinesForSectionTitle(d, section_title); })]).range(["steelblue", "orange"]);
  
  // as a secondary dimension, what fraction of the document consists of security considerations?
  // could encode secondary dimension in color
  
  var svg = d3.select(insertion_selector).insert("svg", "figcaption")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  var circles = svg.selectAll("circle").data(filtered_list).enter().append("circle")
    .attr("cx", function(d){
      return x(new Date(d["date_published"]));
    })
    .attr("cy", function(d){
      if (d["sections"] && d["sections"][section_title]) {
        return y(d["sections"][section_title]);
      } else {
        return y(0);
      }
    })
    .attr("r", 1)
    .style("fill", function(d) {
      var fraction = fractionOfTotalLinesForSectionTitle(d,section_title);
      if (fraction == 0) {
        return "gray";
      }
      return color(fraction);
    });
    
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("right")
      .ticks(5);
  svg.append("g")
      .attr("class", "y axis count")
      .attr("transform", "translate(" + (width - 5) + ", 0)")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "-1em")
      .style("text-anchor", "end")
      .text(label);
    
}

function lineGraphsForSearches(data_list, insertion_selector, search_terms, label) {
  var x = d3.time.scale().domain(d3.extent(data_list, function(d) {return new Date(d["date_published"]);})).nice(d3.time.year).range([0, width]);
  
  var histogram = d3.layout.histogram()
      //.bins(x.ticks(d3.time.month, 3))  // aggregated by quarter
      .bins(x.ticks(d3.time.year, 1)) // aggregated by year
      .value(function(d) { return new Date(d["date_published"]); });
  
  var color = d3.scale.category10();
  
  var lines_data = [];
  search_terms.forEach(function(term) {
    var filtered_list = data_list.filter(function(el){
      return (el[term + "_search"] > 0);
    });
    lines_data.push(histogram(filtered_list));
  });
  
  var data = histogram(data_list);
  
  var y = d3.scale.linear()
    .domain([0,d3.max(data, function(d) { return d.y; })])
    .range([height, 0]);
  
  var y_percentage = d3.scale.linear()
    .domain([0, 1])
    .range([height, 0]);
  
  var line_data = [data];
  window.data = data;
  
  var svg = d3.select(insertion_selector).insert("svg", "figcaption")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);
  
  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(5);
  svg.append("g")
      .attr("class", "y axis count")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(label);
  
  var yAxisRight = d3.svg.axis()
    .scale(y_percentage)
    .orient("right")
    .ticks(5)
    .tickFormat(d3.format("%"));
  svg.append("g")
    .attr("class", "y axis percentage")
    .attr("transform", "translate(" + (width - 5) + ", 0)")
    .call(yAxisRight)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("dy", "-.5em")
    .style("text-anchor", "end")
    .text("Percentage mentioning term");
  
  var deltaX = x(new Date(data[0].x.getTime() + data[0].dx)) / 2;
  deltaX = 0; // don't need to move by half the bin size
  
  var line = d3.svg.line()
    .x(function(d) { return x(d.x) + deltaX; })
    .y(function(d) { return y(d.y); });
  
  var line_percentage = d3.svg.line()
    .x(function(d) { return x(d.x) + deltaX; })
    .y(function(d, i) {
      if (data[i].y == 0) {
        return y_percentage(0);
      }
      return y_percentage(d.y / data[i].y); 
    });
  
  var lines = svg.selectAll(".line").data(line_data)
    .enter()
    .append("path")
    .attr("class", "line")
    .attr("stroke-dasharray", "5,5")
    .attr("d", function(d) { return line(d); })
    .style("stroke", "grey");
  
  var percentage_lines = svg.selectAll(".percentage-line").data(lines_data)
    .enter()
    .append("g");
    
  percentage_lines.append("path")
    .attr("class", "percentage-line")
    .attr("d", function(d) { return line_percentage(d); })
    .style("stroke", function(d) { return color(d); });
  
  percentage_lines.append("text").datum(function(d, i){
    var fraction = Math.round(d.length * .7);
    return {term: search_terms[i], value: d[fraction], fraction: fraction}; })
    //.attr("transform", function(d) { return "translate(" + x(d.value.x) + "," + y_percentage(d.value.y / data[d.fraction].y) + ")"; })
      .attr("x", function(d) {
        return x(d.value.x);
      })
      .attr("y", function(d) {return y_percentage(d.value.y / data[d.fraction].y);})
      .attr("dy", "1em")
      .text(function(d) { return d.term; });
}

function insertHistogramForData(data_list, insertion_selector) {
  var data = d3.layout.histogram()
      .bins(x.ticks(d3.time.month, 1))
      .value(function(d) { return new Date(d["date_published"]); })
      (data_list);

  var y = d3.scale.linear()
      .domain([0, d3.max(data, function(d) { return d.y; })])
      .range([height, 0]);
      
  function transform(d) {
    return "translate(" + x(d.x) + "," + y(d.y) + ")";
  }

  var svg = d3.select(insertion_selector).insert("svg", "figcaption")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var bar = svg.selectAll(".bar")
      .data(data)
    .enter().append("g")
      .attr("class", "bar")
      .attr("transform", transform);

  var barWidth = x(new Date(data[0].x.getTime() + data[0].dx));
  bar.append("rect")
      .attr("x", 1)
      .attr("width", barWidth)
      .attr("height", function(d) { return height - y(d.y); });

  svg.append("g").selectAll("text").data(data).enter().append("text")
      .attr("y", -5)
      .attr("x", x(new Date(data[0].x.getTime() + data[0].dx)) / 2)
      .attr("text-anchor", "middle")
      .attr("transform", transform)
      .attr("class", "label")
      .text(function(d) { return formatCount(d.y); });

  var labels = svg.selectAll("text.label");
  var bounding_boxes = [];
  
  bar.each(function(d, i){
    bounds = this.getBoundingClientRect();
    bounding_boxes.push(bounds);
  });

  labels.each(function(d, i){
    bounds = this.getBoundingClientRect();
    if (bounding_boxes.some(intersectsThis, bounds)) {
      d3.select(this).remove();
    } else {
      bounding_boxes.push(bounds);
    }
  });

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);
  
  // bar.on("mouseover", function(d){
  //   var slist = d3.select(this.parentNode.parentNode.parentNode).select("ul").selectAll("li").data(d);
  //   slist.enter().append("li")
  //     .each(function(){
  //       d3.select(this).insert("a");
  //     });  // add more list items as necessary
  //   
  //   slist.each(function(d){    // if you use .each to insert nested nodes, use .each again to update them
  //     d3.select(this).select("a")
  //       .attr("href", urlFromRFCNumber(d["rfc_number"]))
  //       .text(d["title"]);
  //   });  // make all list items use the appropriate name
  //     
  //   slist.exit().remove();  // remove any list items now unnecessary
  // });
}

function intersectsThis(element, index, array) {
  return intersect(element, this);
}