document.addEventListener('DOMContentLoaded', () => {
    
    // --- Configuration State & DOM Elements ---
    const elements = {
        width: document.getElementById('width'),
        height: document.getElementById('height'),
        margin: document.getElementById('margin'),
        gap: document.getElementById('gap'),
        
        titleText: document.getElementById('titleText'),
        subText: document.getElementById('subText'),
        
        titleSize: document.getElementById('titleSize'),
        subSize: document.getElementById('subSize'),
        labelSize: document.getElementById('labelSize'),
        strokeWidth: document.getElementById('strokeWidth'),
        
        strokeColor: document.getElementById('strokeColor'),
        textColor: document.getElementById('textColor'),
        
        p1Label: document.getElementById('p1Label'),
        p1Color: document.getElementById('p1Color'),
        p2Label: document.getElementById('p2Label'),
        p2Color: document.getElementById('p2Color'),
        p3Label: document.getElementById('p3Label'),
        p3Color: document.getElementById('p3Color'),
        p4Label: document.getElementById('p4Label'),
        p4Color: document.getElementById('p4Color'),
        
        container: document.getElementById('svgContainer'),
        downloadBtn: document.getElementById('downloadBtn'),
        resetBtn: document.getElementById('resetBtn')
    };

    // --- Core Logic (Ported from Python) ---
    function generateSVGString() {
        // 1. Get Values
        const w = parseInt(elements.width.value) || 800;
        const h = parseInt(elements.height.value) || 600;
        const margin = parseInt(elements.margin.value) || 50;
        const gap = parseInt(elements.gap.value) || 20;
        
        const strokeW = parseInt(elements.strokeWidth.value) || 2;
        const strokeC = elements.strokeColor.value;
        const textC = elements.textColor.value;
        const fontSize = parseInt(elements.labelSize.value) || 20;
        
        const titleTxt = elements.titleText.value;
        const titleSize = parseInt(elements.titleSize.value) || 32;
        const subTxt = elements.subText.value;
        const subSize = parseInt(elements.subSize.value) || 18;

        // 2. Layout Calculation
        let headerHeight = 0;
        let titleY = 0;
        let subY = 0;
        let currentY = margin;

        // Font spacing calculation (simulating Python logic)
        if (titleTxt) {
            // In SVG text y is baseline, so we add size to currentY
            titleY = currentY + titleSize; 
            headerHeight += (titleSize * 1.5);
            currentY += (titleSize * 1.5);
        }

        if (subTxt) {
            subY = currentY + subSize;
            headerHeight += (subSize * 1.5);
            currentY += (subSize * 1.5);
        }

        if (headerHeight > 0) {
            headerHeight += 20; // Extra padding
        }

        // 3. Diamond Geometry
        const drawXStart = margin;
        const drawXEnd = w - margin;
        const drawYStart = margin + headerHeight;
        const drawYEnd = h - margin;

        const availW = drawXEnd - drawXStart;
        const availH = drawYEnd - drawYStart;
        const cy = drawYStart + (availH / 2);

        const dWidth = (availW - gap) / 2;
        const pWidth = dWidth / 2;

        const x0 = drawXStart;
        const x1 = x0 + pWidth;
        const x2 = x0 + dWidth;
        const x3 = x2 + gap;
        const x4 = x3 + pWidth;
        const x5 = x3 + dWidth;

        const yTop = drawYStart;
        const yMid = cy;
        const yBot = drawYEnd;

        // Phase Data
        const phases = [
            { 
                label: elements.p1Label.value, 
                color: elements.p1Color.value, 
                d: `M ${x0},${yMid} L ${x1},${yTop} L ${x1},${yBot} Z`, 
                tx: x0 + (pWidth * 0.5) 
            },
            { 
                label: elements.p2Label.value, 
                color: elements.p2Color.value, 
                d: `M ${x1},${yTop} L ${x2},${yMid} L ${x1},${yBot} Z`, 
                tx: x1 + (pWidth * 0.5) 
            },
            { 
                label: elements.p3Label.value, 
                color: elements.p3Color.value, 
                d: `M ${x3},${yMid} L ${x4},${yTop} L ${x4},${yBot} Z`, 
                tx: x3 + (pWidth * 0.5) 
            },
            { 
                label: elements.p4Label.value, 
                color: elements.p4Color.value, 
                d: `M ${x4},${yTop} L ${x5},${yMid} L ${x4},${yBot} Z`, 
                tx: x4 + (pWidth * 0.5) 
            }
        ];

        // 4. Construct SVG
        let svg = `
        <svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">
            <style>
                .phase-text { font-family: Arial, sans-serif; font-size: ${fontSize}px; fill: ${textC}; text-anchor: middle; dominant-baseline: middle; }
                .title { font-family: Arial, sans-serif; font-size: ${titleSize}px; font-weight: bold; fill: ${textC}; text-anchor: middle; }
                .subtitle { font-family: Arial, sans-serif; font-size: ${subSize}px; fill: ${textC}; text-anchor: middle; }
                path { stroke: ${strokeC}; stroke-width: ${strokeW}; stroke-linejoin: round; }
            </style>
            <rect width="100%" height="100%" fill="white" />
        `;

        if (titleTxt) svg += `<text x="${w/2}" y="${titleY}" class="title">${titleTxt}</text>`;
        if (subTxt) svg += `<text x="${w/2}" y="${subY}" class="subtitle">${subTxt}</text>`;

        phases.forEach(p => {
            svg += `
            <path d="${p.d}" fill="${p.color}" />
            <text x="${p.tx}" y="${cy}" class="phase-text">${p.label}</text>`;
        });

        svg += `</svg>`;
        return svg;
    }

    // --- Event Handlers ---

    function updatePreview() {
        const svgContent = generateSVGString();
        elements.container.innerHTML = svgContent;
    }

    function downloadSVG() {
        const svgContent = generateSVGString();
        const blob = new Blob([svgContent], {type: 'image/svg+xml;charset=utf-8'});
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `double-diamond-${Date.now()}.svg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function resetDefaults() {
        // Reload page is easiest way to reset logic without tracking initial state
        if(confirm('Reset all fields to default?')) {
            //location.reload(); --did not work in some browsers e.g. Firefox
            window.location.href = window.location.href;
        }
    }

    // --- Initialization ---

    // Attach listeners to all inputs for real-time update
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', updatePreview);
    });

    elements.downloadBtn.addEventListener('click', downloadSVG);
    elements.resetBtn.addEventListener('click', resetDefaults);

    // Initial Render
    updatePreview();
});