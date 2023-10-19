<script lang="ts">
    import { onMount } from "svelte";
    import { texture } from "./scratchTexture";
    import { brush as brushTexture } from "./brush";
    export let readyToConfetti = false;

    let h: number;
    let w: number;
    let canvas: HTMLCanvasElement;
    onMount(() => {
        // get canvas context
        let isDrawing: boolean = false;
        let lastPoint: { x: number; y: number } = { x: 0, y: 0 };
        let canvasWidth = canvas.width;
        let canvasHeight = canvas.height;
        let ctx = canvas.getContext("2d")!;

        // images price and logo
        let image = new Image() as HTMLImageElement;
        let brush = new Image() as HTMLImageElement;

        image.src = texture;
        brush.src = brushTexture;
        image.onload = function () {
            ctx.drawImage(image, 0, 0, 1024, 576);
        };

        canvas.addEventListener("mousedown", handleMouseDown, false);
        canvas.addEventListener("touchstart", handleMouseDown, false);
        canvas.addEventListener("mousemove", handleMouseMove, false);
        canvas.addEventListener("touchmove", handleMouseMove, false);
        canvas.addEventListener("mouseup", handleMouseUp, false);
        canvas.addEventListener("touchend", handleMouseUp, false);
        type Point = {
            x: number;
            y: number;
        };
        function distanceBetween(point1: Point, point2: Point) {
            return Math.sqrt(
                Math.pow(point2.x - point1.x, 2) +
                    Math.pow(point2.y - point1.y, 2)
            );
        }

        function angleBetween(point1: Point, point2: Point) {
            return Math.atan2(point2.x - point1.x, point2.y - point1.y);
        }

        // Only test every `stride` pixel. `stride`x faster,
        // but might lead to inaccuracy
        function getFilledInPixels(stride: number) {
            if (!stride || stride < 1) {
                stride = 1;
            }

            var pixels = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
            var pdata = pixels.data;
            var l = pdata.length;
            var total = l / stride;
            var count = 0;

            // Iterate over all pixels
            for (var i = (count = 0); i < l; i += stride) {
                // @ts-ignore
                if (parseInt(pdata[i]) === 0) {
                    count++;
                }
            }

            return Math.round((count / total) * 100);
        }

        function getMouse(e, canvas) {
            var offsetX = 0,
                offsetY = 0,
                mx,
                my;

            if (canvas.offsetParent !== undefined) {
                do {
                    offsetX += canvas.offsetLeft;
                    offsetY += canvas.offsetTop;
                } while ((canvas = canvas.offsetParent));
            }

            mx = (e.pageX || e.touches[0].clientX) - offsetX;
            my = (e.pageY || e.touches[0].clientY) - offsetY;

            return { x: mx, y: my };
        }

        function handlePercentage(filledInPixels) {
            filledInPixels = filledInPixels || 0;
            console.log(filledInPixels + "%");
            if (filledInPixels > 50) {
                canvas.parentNode.removeChild(canvas);
                readyToConfetti = true;
            }
        }

        function handleMouseDown(e) {
            isDrawing = true;
            lastPoint = getMouse(e, canvas);
        }

        function handleMouseMove(e) {
            if (!isDrawing) {
                return;
            }

            e.preventDefault();

            var currentPoint = getMouse(e, canvas),
                dist = distanceBetween(lastPoint, currentPoint),
                angle = angleBetween(lastPoint, currentPoint),
                x,
                y;

            for (var i = 0; i < dist; i++) {
                x = lastPoint.x + Math.sin(angle) * i - 25;
                y = lastPoint.y + Math.cos(angle) * i - 25;
                ctx.globalCompositeOperation = "destination-out";
                ctx.drawImage(brush, x, y);
            }

            lastPoint = currentPoint;
            handlePercentage(getFilledInPixels(32));
        }

        function handleMouseUp(e) {
            isDrawing = false;
        }
    });
</script>

<svelte:window bind:innerHeight={h} bind:innerWidth={w} />

<canvas
    class="canvas select-none"
    id="js-canvas"
    width={w / 2}
    height={h / 2}
    bind:this={canvas}
/>
