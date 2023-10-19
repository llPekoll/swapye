<script lang="ts">
    import { fly } from "svelte/transition";
    import type {
        TradDefaults,
        TradIntroOutro,
        TradPrices,
    } from "$lib/interfaces";
    // @ts-ignore
    import { Confetti } from "svelte-confetti";
    import { formSubmited, winner, game } from "$lib/stores";
    import Card from "./Card.svelte";

    export let reload: () => void;

    export let trads: {
        tradDefaults: TradDefaults;
        tradIntroOutro: TradIntroOutro;
        tradPrices: TradPrices;
        langs: string[];
    };

    export let srcBase = "";
    let readyToConfetti = false;

    const ground = `${srcBase}/ground.png`;
    const center = `${srcBase}/center.png`;
    const sides = `${srcBase}/sides.png`;
    const top = `${srcBase}/top.png`;
    const lights = `${srcBase}/lights.png`;
    $: if (formSubmited && $game.automaticRestart) {
        setTimeout(function () {
            reload();
        }, $game.automaticRestartCounterValue * 1000);
    }
    $: if ($formSubmited) {
        readyToConfetti = false;
    }
</script>

<div class="fixed h-screen w-screen">
    {#if $game.bgIngame}
        <img
            src={$game.bgIngame}
            alt="Background"
            class="fixed w-full h-full select-none"
        />
    {/if}
    <img
        src={ground}
        alt="ground"
        class="fixed bottom-0 w-full h-24 select-none"
    />
    {#if $winner.state == "lost"}
        <div
            class="fixed top flex items-center justify-center text-white text-9xl scale-150"
        >
            {trads.tradDefaults.cross}
        </div>
        <div
            class="fixed top flex items-center justify-center text-white text-2xl mt-28"
        >
            {trads.tradDefaults.lost}
        </div>
    {:else if $winner.state == "cant_replay"}
        <div
            class="fixed top flex items-center justify-center text-white text-9xl"
        >
            {trads.tradDefaults.cross}
        </div>
        <div
            class="fixed top flex items-center justify-center text-white text-2xl mt-28"
        >
            {trads.tradDefaults.cant_replay}
        </div>
    {:else if $winner.state == "cant_replay_today"}
        <div
            class="fixed top flex items-center justify-center text-white text-9xl"
        >
            {trads.tradDefaults.cross}
        </div>
        <div
            class="fixed top flex items-center justify-center text-white text-2xl mt-28"
        >
            {trads.tradDefaults.no_more_play_today}
        </div>
    {:else if $winner.state == "won"}
        {#if !$winner.img}
            <div
                class="fixed top flex items-center justify-center text-white text-9xl scale-150"
            >
                🎁
            </div>
        {:else}
            <div class="fixed top flex items-center justify-center">
                <img
                    src={$winner.img}
                    alt="price"
                    class=" max-w-44 aspect-auto max-h-44 price -mt-10"
                />
            </div>
        {/if}
    {/if}
    <img
        src={lights}
        alt="lights"
        class="fixed bottom-0 w-full h-full lights select-none"
    />
    {#if $winner.state !== "lost" && $winner.displayTitle}
        {#if $winner.name}
            <div
                class="fixed top flex items-center justify-center text-white text-3xl mt-40 {$winner.offsetTitle}"
            >
                {$winner.name}
            </div>
        {/if}
    {/if}
    {#if trads.tradIntroOutro.closingText}
        <div
            class="fixed top flex items-center justify-center text-white text-3xl mt-40"
        >
            {@html trads.tradIntroOutro.closingText}
        </div>
    {/if}
    {#if $formSubmited}
        <div class="fixed top-1/4 left-1/4">
            <Card bind:readyToConfetti />
        </div>
    {/if}
    {#if !$formSubmited}
        <div
            out:fly={{ y: -1000, duration: 2000, delay: 1000 }}
            class="fixed -top-10 left-0 w-full h-full"
        >
            <img class="w-full h-full" alt="center curtain" src={center} />
            <div
                class="fixed top-0 flex items-center justify-center w-full h-full"
            >
                <img
                    class="logo max-w-44 max-h-44"
                    alt="Logo"
                    src={$game.logo}
                />
            </div>
        </div>
    {/if}
    {#if $formSubmited && readyToConfetti && $winner.state == "won"}
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

    {#if $formSubmited && $game.restartBtn}
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
