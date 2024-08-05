import bwipjs from 'bwip-js';
import cheerio from 'cheerio';
import fs from 'fs';
import path from 'path';
import puppeteer from "puppeteer";

const datamatrixText = process.argv[2];
const serial = process.argv[3];
const template = process.argv[4];

( async () => {
    const templateDir = `/src/${template}`;
    const text = "esto es una prueba";
    const pngData = await bwipjs.toBuffer({
        bcid:        'datamatrix',       // Barcode type
        text:        datamatrixText,    // Text to encode
        scale:       3,               // 3x scaling factor
        width:       5,              // Adjust width as needed
        height:      5,              // Bar height, in millimeters
        includetext: false,            // Show human-readable text
        textxalign:  'center',        // Always good to set this
    })
    const templatePath = path.join(templateDir, 'input.html')

    const htmlContent = fs.readFileSync(templatePath, 'utf-8');

    const $ = cheerio.load(htmlContent);
    // Replace image URLs with Base64 data
    $('img').each((index, element) => {
      const imageUrl = $(element).attr('src');

      if(!imageUrl) return;

      if (!(imageUrl.startsWith('http') || imageUrl.startsWith('data:image'))) {
        const base64Data = getLocalImageBase64(path.join(templateDir,imageUrl))
        $(element).attr('src', base64Data);
        console.log('The image was created successfully!')
      }
    });

    $('#Serial').text(serial);



    const modifiedHtml = $.html();    
    const outputTpl = `/src/output/${serial}_${template}`
    fs.writeFileSync(`${outputTpl}.html`, modifiedHtml)

    const outputPath = `${outputTpl}.png`;
    try {
      

      const browser = await puppeteer.launch({
        defaultViewport: null,
     args: [
      '--no-sandbox', '--disable-gpu', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });
      const page = await browser.newPage();
      const targetWidthMM = 12;
      const targetHeightMM = 15;

      const devicePixelRatio = await page.evaluate(() => window.devicePixelRatio);

      // Convert mm to pixels
     const targetWidthPx = targetWidthMM * devicePixelRatio;
     const targetHeightPx = targetHeightMM * devicePixelRatio;
     await page.setViewport({width: 0, height: 0, deviceScaleFactor: 7.5});

      await page.waitForSelector('body')




      await page.setContent(modifiedHtml);

      const content = await page.$("body");
      if(content) {

        


        const imageBuffer = await content.screenshot();
        fs.writeFileSync(outputPath,imageBuffer)

      }

    
      await page.close();
      await browser.close();

    

    } catch (error) {
      console.log("🔥🔥🔥  ERROR: ", error)
    }

    
    
    
    
    
    console.log("ok")
})()

