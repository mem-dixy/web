
exports.__esModule = true;
const _0000_007F_1 = exports,
    EventListener_1 = exports,
    EventType_1 = exports,
    rune_1 = exports;
/* eslint-disable max-statements */
/* eslint-disable no-magic-numbers */
/* eslint-disable no-undef */
/* eslint-disable one-var */
/* eslint-disable prefer-const */
/* eslint-disable sort-vars */
let canvas = document.getElementsByTagName("canvas");
let data = null,
    indexX = 0,
    indexY = 0,
    off = 0,
    view = null;

/**
 * @param {HTMLCanvasElement} element
 */
let spat = function spat (element) {

    let context = element.getContext("2d"),
        {width} = element,
        {height} = element,
        imageData = context.createImageData(width, height);
    let yy = height;
    while (yy > 0) {

        yy -= 1;
        let xx = width;
        while (xx > 0) {

            xx -= 1;
            let index = imageData.width;
            index *= yy;
            index += xx;
            index *= 4;
            imageData.data[index + 0] = Math.random() * 256;
            imageData.data[index + 1] = Math.random() * 256;
            imageData.data[index + 2] = Math.random() * 256;
            imageData.data[index + 3] = 255;

        }

    }
    context.putImageData(imageData, 0, 0);
    return imageData;

    /*
     *Index_x = 25;
     *indexY = 25;
     *context.putImageData(imageData, 0, 0, indexX, indexY, 8, 8);
     */

};

/**
 * @param {HTMLCanvasElement} element
 */
let main = function main (element) {

    view = element.getContext("2d");
    data = view.createImageData(element.width, element.height);
    data = spat(element);
    view.putImageData(data, 0, 0);

};
spat(canvas[0]);
spat(canvas[1]);
spat(canvas[2]);
spat(canvas[3]);
spat(canvas[4]);
spat(canvas[5]);
spat(canvas[6]);
spat(canvas[7]);
main(canvas[3]);

/**
 * @param {any[] | Uint8Array} art
 */
let draw = function draw (art) {

    let hold1 = 0x100 - indexY,
        // eslint-disable-next-line no-bitwise
        hold2 = hold1 << 0x3,
        hold3 = hold2 - 0x1,
        // eslint-disable-next-line no-bitwise
        hold4 = hold3 << 0x8,
        hold5 = hold4 + indexX,
        // eslint-disable-next-line no-bitwise
        hold6 = hold5 << 0x5,
        hold7 = hold6;
    let index = 256;
    while (index > 0) {

        index -= 1;
        // eslint-disable-next-line no-bitwise
        let temp1 = index & 31,
            // eslint-disable-next-line no-bitwise
            temp2 = index >>> 5,
            // eslint-disable-next-line no-bitwise
            temp3 = temp2 << 13,
            temp4 = hold7 + temp1 - temp3;
        data.data[temp4] = art[index];

    }
    view.putImageData(data, 0, 0);

};

/**
 * @param {number} input
 */
let paint64 = function paint64 (input) {

    let glyph = input,
        index = 256;
    // eslint-disable-next-line no-undef
    let art = new Uint8Array(index);
    let bb = Math.random(),
        gg = Math.random(),
        rr = Math.random();
    bb *= 128;
    gg *= 128;
    rr *= 128;
    bb += 128;
    gg += 128;
    rr += 128;
    while (index >= 0) {

        index -= 4;
        // eslint-disable-next-line no-bitwise
        let bit = glyph & 1;
        art[index + 0] = rr * bit;
        art[index + 1] = gg * bit;
        art[index + 2] = bb * bit;
        art[index + 3] = 255;
        // eslint-disable-next-line no-bitwise
        glyph >>>= 1;

    }
    return art;

};
EventListener_1.EventListener.SelectFirstEventTargetBubblePhaseInvokeLater("body", EventType_1.EventType.KeyboardEvent.keypress, (item) => {

    let key = item;
    let char = key.keyCode;
    let code = _0000_007F_1.character.range_0000_007F[char];
    let glyph = rune_1.font.rune[code];
    if (typeof glyph !== "undefined") {

        draw(paint64(glyph));

    }
    indexX += 0;
    indexY += 1;

});

/**
 * @param {number} glyph
 */
let out = function out (glyph) {

    draw(paint64(glyph));
    indexX += 1;
    off += 1;
    if (off % 8 === 0) {

        off = 0;
        indexX -= 8;
        indexY += 1;

    }
    if (indexY > 254) {

        indexY = 0;
        indexX += 9;

    }

};
out(0xFEA0BE80FE808000);
out(0xFE222E2A2A2A2A00);
out(0x0202FE02FA0AFE00);
out(0xA8A8A8A8E888FE00);
out(0xFE0AFA02FE020200);