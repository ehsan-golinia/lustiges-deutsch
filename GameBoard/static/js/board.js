// Define the exact positions of the cells in the board layout
  const boardData = [
    { value: '• •', x: 2, y: 6, special: 'start' },
    { value: 'Start', x: 2, y: 6, special: 'start' },
    { value: 1, x: 2, y: 5 },
    { value: 2, x: 2, y: 4 },
    { value: 3, x: 2, y: 3 },
    { value: 4, x: 2, y: 2 },
    { value: 5, x: 2, y: 1 },
    { value: 6, x: 2, y: 0 },
    { value: 7, x: 3, y: 0 },
    { value: 8, x: 4, y: 0 },
    { value: 9, x: 4, y: 1 },
    { value: 10, x: 4, y: 2 },
    { value: 11, x: 4, y: 3 },
    { value: 12, x: 4, y: 4 },
    { value: 13, x: 4, y: 5 },
    { value: 14, x: 4, y: 6 },
    { value: 15, x: 5, y: 6 },
    { value: 16, x: 6, y: 6 },
    { value: 17, x: 6, y: 5 },
    { value: 18, x: 6, y: 4 },
    { value: 19, x: 6, y: 3 },
    { value: 20, x: 6, y: 2 },
    { value: 21, x: 6, y: 1 },
    { value: 22, x: 6, y: 0 },
    { value: 23, x: 7, y: 0 },
    { value: 24, x: 8, y: 0 },
    { value: 25, x: 8, y: 1 },
    { value: 26, x: 8, y: 2 },
    { value: 27, x: 8, y: 3 },
    { value: 28, x: 8, y: 4 },
    { value: 29, x: 8, y: 5 },
    { value: 'End', x: 8, y: 6, special: 'end' },
  ];

  const cellSize = 50;

  // Create the SVG board
  const svg = d3.select('#board');

  // Draw cells
  svg.selectAll('.cell')
    .data(boardData)
    .enter()
    .append('rect')
    .attr('class', (d) => `cell ${d.special || ''}`)
    .attr('x', (d) => d.x * cellSize)
    .attr('y', (d) => d.y * cellSize)
    .attr('width', cellSize)
    .attr('height', cellSize)
    .on('click', (event, d) => alert(`You clicked on ${d.value}`));

  // Add text labels
  svg.selectAll('text')
    .data(boardData)
    .enter()
    .append('text')
    .attr('x', (d) => d.x * cellSize + cellSize / 2)
    .attr('y', (d) => d.value === '• •' ? d.y * cellSize + cellSize : d.y * cellSize + cellSize / 2)
    .text((d) => d.value)
    .style('pointer-events', 'none') // Prevent text from blocking clicks
    .style('font-size', (d) => (d.value === '• •' ? '30px' : '14px'))
    .style('fill', (d) => (d.value === '• •' ? '#ff6347' : '#385170'));
