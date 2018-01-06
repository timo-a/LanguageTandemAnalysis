convert_links = function(graph){
graph.links = graph.links.map(l => {
    var sourceNode = graph.nodes.filter(n => { return n.name === l.source; })[0],
        targetNode = graph.nodes.filter(n => { return n.name === l.target; })[0];

    return {
        source: sourceNode,
        target: targetNode,
        value: l.value
    };
   });
   return graph
}

do_graph = function(svg_id, graph){

graph = convert_links(graph)

var width = 960;
var height = 500;
var margin = 20;
var pad = margin / 2;
var tooltips = null;
var labels = null;
drawGraph(graph);

function drawGraph(graph) {
  var svg = d3.select(svg_id)//.append("svg")
                             .attr("width", width)
                             .attr("height", height);
  // draw plot background
  svg.append("rect")
     .attr("width", width)
     .attr("height", height)
     .style("fill", "#f3f3f3");

  // create an area within svg for plotting graph
  var plot = svg.append("g")
                .attr("id", "plot")
                .attr("transform", "translate(" + pad + ", " + pad + ")");

  // https://github.com/mbostock/d3/wiki/Force-Layout#wiki-force
  var layout = d3.layout.force()
                        .size([width - margin, height - margin])
                        .charge(-400)
                        .linkDistance(70)
                        .nodes(graph.nodes)
                        .links(graph.links)
                        .start();

  drawLinks(graph.links, svg);
  drawNodes(graph.nodes, svg);
  var drag = layout.drag().on("dragstart", dragstart);

  // add ability to drag and update layout
  // https://github.com/mbostock/d3/wiki/Force-Layout#wiki-drag
  svg.selectAll(".node").call(drag);

  // https://github.com/mbostock/d3/wiki/Force-Layout#wiki-on
  layout.on("tick", tick);

  function tick() {
    svg.selectAll(".link")
      .attr("x1", d => { return d.source.x; })
      .attr("y1", d => { return d.source.y; })
      .attr("x2", d => { return d.target.x; })
      .attr("y2", d => { return d.target.y; });

    tooltips
      .attr("x", (d, i) => { return d.x + 10;  })
      .attr("y", (d, i) => { return d.y - 10;  });
    
    svg.selectAll(".node")
      .attr("cx", d => { return d.x; })
      .attr("cy", d => { return d.y; });

    labels.attr("x", d => { return (d.source.x + d.target.x) / 2; }) 
          .attr("y", d => { return (d.source.y + d.target.y) / 2; })

      
  }
}

  function dblclick(d)  { d3.select(this).classed("fixed", d.fixed = false);}

  function dragstart(d) { d3.select(this).classed("fixed", d.fixed = true);}

// Draws nodes on plot
function drawNodes(nodes, svg) {

  // https://github.com/mbostock/d3/wiki/Force-Layout#wiki-nodes
  tooltips = svg.select("#plot").selectAll(".node")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("class", "node")
    .attr("id", (d, i) =>  {  return d.name;  })
    .attr("cx", (d, i) =>  {  return d.x;  })
    .attr("cy", (d, i) =>  {  return d.y;  })
    .attr("r", 12)
//    .style("fill", (d, i) =>  {  return color(1);  }) color
    .on("dblclick", dblclick)

    .select(function() { return this.parentNode })
    .append('text')
    .data(nodes)
    .text(function(d) { return d.name; })
    .attr("x", (d, i) => { return d.x;  })
    .attr("y", (d, i) => { return d.y;  })
    .attr("class", "d3-tooltip")
    .attr("id", function(d,i) { return "tooltip-" + i; });

}

// Draws edges between nodes
function drawLinks(links, svg) {
  var scale = d3.scale.log()
                 .domain(d3.extent(links, (d, i) => { return d.value; }))
                 .range([1, 6]);

  // https://github.com/mbostock/d3/wiki/Force-Layout#wiki-links
  svg.select("#plot").selectAll(".link")
     .data(links)
     .enter()
     .append("line")
     .attr("class", "link")
     .attr("x1", d => { return d.source.x; })
     .attr("y1", d => { return d.source.y; })
     .attr("x2", d => { return d.target.x; })
     .attr("y2", d => { return d.target.y; })
     .style("stroke-width", (d, i) => { return scale( d.value ) + "px"; });

  labels= svg.select("#plot").selectAll("text")
  .data(links)  
     .enter()
     .append("text")
     .text(d => { return d.value;})
    .attr("x", d => { return (d.source.x + d.target.x) / 2; })
     .attr("y", d => { return (d.source.y + d.target.y) / 2; })
     .style("font-family", 'times')
         //.attr("dy", -r * 2)
     .attr("id", "label");
  



}

}
do_graph("#force_within_search", graphs.within_search);
do_graph("#force_within_offer",  graphs.within_offer);
  //  dobi_graph();
