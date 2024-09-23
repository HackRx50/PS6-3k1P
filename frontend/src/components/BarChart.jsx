import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const BarChart = ({ data, width, height, valueKey }) => {
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

    const margin = { top: 20, right: 30, bottom: 40, left: 40 };

    const x = d3.scaleBand()
      .domain(processedData.map(d => d.value))
      .range([margin.left, width - margin.right])
      .padding(0.1);

    const y = d3.scaleLinear()
      .domain([0, d3.max(processedData, d => d.count)]).nice()
      .range([height - margin.bottom, margin.top]);

    const svg = d3.select(ref.current)
      .attr("viewBox", [0, 0, width, height]);

    svg.selectAll("*").remove(); // Clear previous content

    svg.append("g")
      .attr("fill", "steelblue")
      .selectAll("rect")
      .data(processedData)
      .join("rect")
      .attr("x", d => x(d.value))
      .attr("y", d => y(d.count))
      .attr("height", d => y(0) - y(d.count))
      .attr("width", x.bandwidth());

    svg.append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickFormat(d3.format("d")))
      .attr("font-size", '10px'); // Reduced font size

    svg.append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .attr("font-size", '10px'); // Reduced font size

  }, [data, width, height, valueKey]);

  return <svg ref={ref}></svg>;
};

export default BarChart;