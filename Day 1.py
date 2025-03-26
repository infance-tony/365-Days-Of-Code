function generatePDF(responseData, filePath = 'output.pdf') {
    const doc = new PDFDocument({ size: 'A4', margin: 50 });
    const stream = fs.createWriteStream(filePath);
    doc.pipe(stream);

    // **Header Image (Top)**
    const headerHeight = 80; // Adjust as needed
    doc.image('header.png', 0, 0, { width: doc.page.width, height: headerHeight });

    // **Footer Image (Bottom)**
    const footerHeight = 80; // Adjust as needed
    doc.image('footer.png', 0, doc.page.height - footerHeight, { width: doc.page.width, height: footerHeight });

    // **Adjust Content Position (To Avoid Overlap)**
    let contentStartY = headerHeight + 20; // Push content below the header
    let contentEndY = doc.page.height - footerHeight - 20; // Stop content before footer

    // **Company Title & Info**
    doc.fillColor('#004E91').fontSize(24).text('Memco', 50, contentStartY, { bold: true });
    doc.fontSize(14).text('Membrane Guru (Reverse Osmosis Antiscalant Software)', 50, contentStartY + 30);

    // **HCL Dosing Results Section**
    let sectionStartY = contentStartY + 70;
    doc.fillColor('#004E91').fontSize(20).text('HCL Dosing Results', 50, sectionStartY);
    doc.moveDown();
    doc.fillColor('black').fontSize(16);
    doc.text(`PH - Feed Water: ${responseData.input.inputValues.PH}`);
    doc.text(`PH - After Adjust: ${responseData.output.ph_and_hcl_dose.PH}`);
    doc.text(`HCL Dosage: ${responseData.output.ph_and_hcl_dose.HCL_dose} mg/liter`);
    doc.text(`HCL requirement for M: ${responseData.output.ph_and_hcl_dose.HCL_dose} hour`);

    // **Product Section**
    doc.moveDown(1);
    doc.rect(50, doc.y + 10, 500, 80).fill('#D6F0FF');
    doc.fillColor('black').fontSize(14).text('Recommended Product', 60, doc.y + 20);
    doc.fontSize(20).fillColor('#000').text(`  ${responseData.output.product}`, 250, doc.y - -2, { bold: true });

    // **Ensure Content Doesn't Overlap Footer**
    if (doc.y > contentEndY) {
        doc.addPage();
        doc.y = headerHeight + 20; // Reset content position on new page
    }

    // **Dosing Details**
    doc.fillColor('#004E91').fontSize(20).text('Product Dosing Details', 50);
    doc.moveDown();
    doc.fillColor('black').fontSize(16);
    doc.text(`Dosing pump ratio: ${responseData.output.pump_ratio.Dosing_Pump_Ratio} nos`);
    doc.text(`Water: ${responseData.output.water_in_litres} liter`);
    doc.text(`Antiscalant: ${responseData.output.antiscalant.Antiscalant} liter`);

    doc.end();
    console.log(`Styled PDF saved at ${filePath}`);
}
