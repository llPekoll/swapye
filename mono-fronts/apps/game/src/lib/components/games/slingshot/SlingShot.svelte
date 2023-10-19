<script lang="ts">
    import { fly } from "svelte/transition";
    import type {
        TradDefaults,
        TradIntroOutro,
        TradPrices,
    } from "$lib/interfaces";
    import { Confetti } from "svelte-confetti";
    import { formSubmited, winner, game } from "$lib/stores";
    import Matter from "matter-js";
    import { onMount } from "svelte";
    export let reload: () => void;
    export let trads: {
        tradDefaults: TradDefaults;
        tradIntroOutro: TradIntroOutro;
        tradPrices: TradPrices;
        langs: string[];
    };
    export let srcBase = "";
    let h: number;
    let w: number;
    onMount(() => {
        h = window.innerHeight;
        w = window.innerWidth;
        createScene();
    });
    function createScene() {
        var Engine = Matter.Engine,
            Render = Matter.Render,
            Runner = Matter.Runner,
            Composites = Matter.Composites,
            Events = Matter.Events,
            Constraint = Matter.Constraint,
            MouseConstraint = Matter.MouseConstraint,
            Mouse = Matter.Mouse,
            Composite = Matter.Composite,
            Bodies = Matter.Bodies;

        // create an engine
        var engine = Engine.create();
        var world = engine.world;

        // create a renderer

        console.log("sako", w);
        var render = Render.create({
            element: document.getElementById("matter-js"),
            engine: engine,
            options: {
                width: w,
                height: h,
                showAngleIndicator: false,
                pixelRatio: 1,
                background: "rgba(0, 0, 0, 0)",
                hasBounds: false,
                enabled: true,
                wireframes: false,
                showSleeping: true,
            },
        });

        // run the renderer
        Matter.Render.run(render);

        // create runner
        var runner = Runner.create();

        // run the engine
        Matter.Runner.run(runner, engine);

        // add bodies
        var ground = Bodies.rectangle(w / 2, h, w, 50, {
                isStatic: true,
                render: { fillStyle: "#060a19" },
            }),
            rockOptions = { density: 0.004 },
            rock = Bodies.circle(w / 4, 450, 30, rockOptions),
            anchor = { x: w / 4, y: 450 },
            elastic = Constraint.create({
                pointA: anchor,
                bodyB: rock,
                stiffness: 0.05,
            });

        var ground2 = Bodies.rectangle(w / 2 + w / 5, h - 300, w / 2, 20, {
            isStatic: true,
            render: { fillStyle: "#060a19" },
        });
        var pyramid2 = Composites.pyramid(
            w / 2,
            h / 4,
            20,
            20,
            0,
            0,
            function (x: number, y: number) {
                return Bodies.rectangle(x, y, 40, 40);
            }
        );
        Composite.add(engine.world, [ground, ground2, pyramid2, rock, elastic]);
        Events.on(engine, "afterUpdate", function () {
            if (
                mouseConstraint.mouse.button === -1 &&
                (rock.position.x > w / 4 + 20 || rock.position.y < 430)
            ) {
                rock = Bodies.circle(w / 4, 450, 30, rockOptions);
                Composite.add(engine.world, rock);
                elastic.bodyB = rock;
            }
        });

        // add mouse control
        var mouse = Mouse.create(render.canvas),
            mouseConstraint = MouseConstraint.create(engine, {
                mouse: mouse,
                constraint: {
                    stiffness: 0.2,
                    render: {
                        visible: false,
                    },
                },
            });

        Composite.add(world, mouseConstraint);

        // keep the mouse in sync with rendering
        render.mouse = mouse;
    }
    const ground = `${srcBase}/ground.png`;
    const center = `${srcBase}/center.png`;
    const sides = `${srcBase}/sides.png`;
    const top = `${srcBase}/top.png`;
    const lights = `${srcBase}/lights.png`;
    $: if ($formSubmited && $game.automaticRestart) {
        setTimeout(function () {
            reload();
        }, $game.automaticRestartCounterValue * 1000);
    }
</script>

<svelte:window bind:innerHeight={h} bind:innerWidth={w} />

<div class="fixed h-screen w-screen">
    {#if $game.bgIngame}
        <img class="fixed w-full h-full" alt="Logo" src={$game.bgIngame} />
    {/if}
    <img src={ground} alt="sides" class="fixed bottom-0 w-full h-full" />
    {#if $winner.state == "lost"}
        <div
            class="fixed top flex items-center justify-center text-white text-9xl scale-150"
        >
            {trads[0].cross}
        </div>
        <div
            class="fixed top flex items-center justify-center text-white text-2xl mt-28"
        >
            {trads[0].lost}
        </div>
    {:else if winner.state == "cant_replay"}
        <div
            class="fixed top flex items-center justify-center text-white text-9xl"
        >
            {trads[0].cross || "🚫"}
        </div>
        <div
            class="fixed top flex items-center justify-center text-white text-2xl mt-28"
        >
            {trads[0].cant_replay || "Vous ne pouvez pas rejouer"}
        </div>
    {:else if winner.state == "cant_replay_today"}
        <div
            class="fixed top flex items-center justify-center text-white text-9xl"
        >
            {trads[0].cross || "🚫"}
        </div>
        <div
            class="fixed top flex items-center justify-center text-white text-2xl mt-28"
        >
            {trads[0].no_more_play_today ||
                "Vous ne pouvez pas rejouer Aujourd'hui"}
        </div>
    {:else if winner.state == "won"}
        {#if !winnerTrad.img}
            <div
                class="fixed top flex items-center justify-center text-white text-9xl scale-150"
            >
                🎁
            </div>
        {:else}
            <div class="fixed top flex items-center justify-center">
                <img
                    src={winnerTrad.img}
                    alt="price"
                    class=" max-w-44 aspect-auto max-h-44 price -mt-10"
                />
            </div>
        {/if}
    {/if}
    <img src={lights} alt="sides" class="fixed bottom-0 w-full h-full lights" />
    {#if winner.state !== "lost" && winner.displayTitle}
        {#if winnerTrad.name}
            <div
                class="fixed top flex items-center justify-center text-white text-3xl mt-20 {winner.offsetTitle}"
            >
                {winnerTrad.name}
            </div>
        {/if}
    {/if}
    {#if trads[1].closing_text}
        <div
            class="fixed top flex items-center justify-center text-white text-3xl mt-40"
        >
            {@html trads[1].closing_text}
        </div>
    {/if}
    {#if !formSubmited}
        <div
            out:fly={{ y: -1000, duration: 4000, delay: 1000 }}
            class="fixed top-0 left-0 w-full h-full"
        >
            <img class="w-full h-full" alt="center curtain" src={center} />
            <div
                class="fixed top-0 flex items-center justify-center w-full h-full"
            >
                <img class="logo max-w-44 max-h-44" alt="Logo" src={logo} />
            </div>
        </div>
    {/if}
    {#if formSubmited}
        <div class="confetti">
            <Confetti
                x={[-5, 5]}
                y={[0, 0.1]}
                delay={[500, 2000]}
                duration={5000}
                amount={400}
                fallDistance="100vh"
            />
        </div>
    {/if}

    <div class="flex justify-center">
        <div id="matter-js" class="z-10" />
    </div>
    <img src={sides} alt="sides" class=" h-full fixed top-0 select-none" />
    <img
        src={sides}
        alt="sides"
        class=" h-full fixed top-0 right-0 -scale-x-100 select-none"
    />
    <img
        src={top}
        alt="sides"
        class="fixed top-0 w-full scale-y-150 md:scale-y-100 select-none"
    />
    {#if formSubmited && restartBtn}
        <div
            in:fly={{ y: -100, delay: 3000 }}
            on:click={reload}
            on:keypress={reload}
            class=" fixed top-10 right-10 text-white"
        >
            <svg width="4em" height="4em" viewBox="0 0 20 20"
                ><path
                    fill="currentColor"
                    d="M14.66 15.66A8 8 0 1 1 17 10h-2a6 6 0 1 0-1.76 4.24l1.42 1.42zM12 10h8l-4 4l-4-4z"
                /></svg
            >
        </div>
    {/if}
    <div class="bg" />
</div>

<style lang="postcss">
    div {
        font-family: century-gothic, sans-serif;
    }
    .lights {
        mix-blend-mode: screen;
    }
    .logo {
        mix-blend-mode: multiply;
    }
    .bg {
        background-color: black;
        width: 100vw;
        height: 100vh;
    }
    img {
        background: transparent;
        user-drag: none;
        -moz-user-select: none;
        -webkit-user-drag: none;
        -webkit-user-select: none;
        -ms-user-select: none;
    }
    .top {
        width: 100vw;
        height: 100vh;
    }
    .confetti {
        position: fixed;
        top: -50px;
        left: 0;
        height: 100vh;
        width: 100vw;
        display: flex;
        justify-content: center;
        overflow: hidden;
        pointer-events: none;
    }
</style>
