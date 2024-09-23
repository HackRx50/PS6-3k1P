import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const PieChart = ({ data, width, valueKey }) => {
  const ref = useRef();

  useEffect(() => {
    // Preprocess the data to count occurrences of each valueKey
    const valueCounts = Array(6).fill(0); // Initialize an array for values 0 to 5
    data.forEach(item => {
      if (item[valueKey] >= 0 && item[valueKey] <= 5) {
        valueCounts[item[valueKey]]++;
      }
    });

    const processedData = valueCounts.map((count, value) => ({ value, count }));

    const height = Math.min(300, width / 2); // Reduced height
    const outerRadius = height / 2 - 10;
    const innerRadius = outerRadius * 0.75;
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const svg = d3.select(ref.current)
      .attr("viewBox", [-width / 2, -height / 2, width, height]);

    const arc = d3.arc()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius);

    const pie = d3.pie().sort(null).value(d => d.count);

    const path = svg.selectAll("path")
      .data(pie(processedData))
      .join("path")
      .attr("fill", (d, i) => color(d.data.value))
      .attr("d", arc)
      .each(function (d) { this._current = d; });

    function arcTween(a) {
      const i = d3.interpolate(this._current, a);
      this._current = i(0);
      return t => arc(i(t));
    }

    function change(value) {
      pie.value(d => d[value]);
      path.data(pie(processedData));
      path.transition().duration(750).attrTween("d", arcTween);
    }

    // Attach the change function to the svg node
    const svgNode = svg.node();
    svgNode.change = change;

    // Cleanup function
    return () => {
      svg.selectAll("*").remove();
    };
  }, [data, width, valueKey]);

  return <svg ref={ref}></svg>;
};

export default PieChart;
