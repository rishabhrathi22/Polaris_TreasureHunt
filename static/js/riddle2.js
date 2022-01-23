let canvas, ctx, flag = 0;
let color = "rgba(28,239,194,0.1)"
let radius = 28
let pointArray = []

const init = () => {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext("2d");
    w = canvas.width;
    h = canvas.height

    canvas.addEventListener("mousemove", function (e) {
        drawCircle(e)
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        flag = 1
        drawCircle(e)
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        flag = 0
        drawCircle(e)
    }, false);
    canvas.addEventListener("mouseout", function (e) {
        flag = 0
        drawCircle(e)
    }, false);
}

const erase = () => {
    pointArray = []
    ctx.clearRect(0, 0, w, h);
}

const drawCircle = (e) => {

    if (flag == 0) return;

    currX = e.clientX - canvas.offsetLeft;
    currY = e.clientY - canvas.offsetTop;

    // circle
    ctx.beginPath();
    ctx.arc(currX, currY, radius, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}

window.onload = () => {
    init()
}