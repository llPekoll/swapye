<script lang="ts">
    import Caption from "./Caption.svelte";
    // @ts-ignore
    import { Confetti } from "svelte-confetti";
    import { fly } from "svelte/transition";
    import { gameResult } from "$lib/algo";
    import type {
        TradDefaults,
        TradIntroOutro,
        TradPrices,
    } from "$lib/interfaces";
    import { formSubmited, winner, game } from "$lib/stores";

    interface Price {
        id: number;
        type: "image" | "text";
        value: string;
        tradPacks: {
            value: string;
            lang: string;
        }[];
    }

    interface Reel {
        style: string;
        className: string;
        price: Price;
    }

    export let reloadSlot: () => void;
    export let trads: {
        tradDefaults: TradDefaults;
        tradIntroOutro: TradIntroOutro;
        tradPrices: TradPrices;
        langs: string[];
    };
    export let state = "idle";
    export let lang = "fr";
    export let srcBase = "";
    export let prices: Price[] = [];

    let readyToRestart = false;

    let winnerPrice: Price = {
        id: 0,
        type: "image",
        value: "",
        tradPacks: [
            {
                value: "",
                lang: "fr",
            },
        ],
    };
    console.log("PRIOCE !");
    console.log(prices);
    console.log("PRIOCE 121212");
    prices = prices.prices;
    console.log(prices);
    const idPriceList = prices.map((price): number => {
        return price.id;
    });
    console.log("idPriceList");
    console.log(idPriceList);

    const ids = gameResult(idPriceList);
    const price1Start = prices.filter((price) => price.id === ids[0])[0];
    const price2Start = prices.filter((price) => price.id === ids[1])[0];
    const price3Start = prices.filter((price) => price.id === ids[2])[0];

    let reels: Reel[] = [
        {
            className: "reel reel-left",
            style: "margin-top: 0px;",
            price: price1Start,
        },
        { className: "reel reel-center", style: "", price: price2Start },
        { className: "reel reel-right", style: "", price: price3Start },
    ];
    console.log("reels");
    console.log(reels);
    let stick = "down";
    const reelSize = 142;
    let showPrice = false;
    let winnerReelsPrice = false;
    $: if ($formSubmited) {
        console.log("win state", $winner.state);
        state = "idle";
        let longestTempo = 0;
        const reelsLength = reels.length;

        if ($winner.state == "won") {
            console.log("$$$$$$$$$$$$winner$$$$$$$$$$");
            console.log($winner);
            winnerPrice = prices.filter(
                (price) => price.id === $winner.price
            )[0];
            console.log("winnerPrice", winnerPrice);
            reels[0].price = winnerPrice;
            reels[1].price = winnerPrice;
            reels[2].price = winnerPrice;
            winnerReelsPrice = true;
        } else {
            const price1 = prices.filter((price) => price.id === ids[0])[0];
            const price2 = prices.filter((price) => price.id === ids[1])[0];
            const price3 = prices.filter((price) => price.id === ids[2])[0];
            reels[0].price = price1;
            reels[1].price = price2;
            reels[2].price = price3;
            winnerReelsPrice = true;
        }
    }

    const getWidth = (size: number, screens: Array<number[]>): number => {
        for (let i = 0; i < screens.length - 1; ++i) {
            if (size <= screens[i][0]) {
                return screens[i][1];
            }
        }
        return screens[screens.length - 1][1];
    };
    const screens = [
        [600, 67],
        [1279, 111],
        [10000, 142],
    ];

    function onClick() {
        if (!$formSubmited) {
            return;
        }
        const reelSize: number = getWidth(innerWidth, screens) * 2;
        if (state !== "idle") {
            return false;
        }
        stick = "up";
        state = "busy";
        let winner = [35, 35, 35];
        let longestTempo = 0;
        const reelsLength = reels.length;
        for (let i = 0; i < reelsLength; ++i) {
            let calc = reelSize * 28.5;
            // let calc = reelSize * (winner[i] + 35);
            let tempo = Math.round(Math.random() * 2000) + 1000;
            longestTempo = tempo > longestTempo ? tempo : longestTempo;
            reels[
                i
            ].style = `margin-top: -${calc}px; transition-duration: ${tempo}ms;`;
        }
        setTimeout(function () {
            stick = "down";
            state = "end";
        }, 250);
        setTimeout(function () {
            showPrice = true;
        }, 4000);
        setTimeout(function () {
            readyToRestart = true;
        }, 4500);
    }
    const reload = () => {
        reloadSlot();
        showPrice = false;
        readyToRestart = false;
    };
    $: if ($formSubmited && $game.automaticRestart) {
        setTimeout(function () {
            reload();
        }, $game.automaticRestartCounterValue * 1000 + 4500);
    }
    $: if ($winner !== undefined) {
        if (
            $winner.state == "cant_replay" ||
            $winner.state == "cant_replay_today"
        ) {
            showPrice = true;
            readyToRestart = true;
        }
    }

    const ground = `${srcBase}/01A_ground.png`;
    const curtain = `${srcBase}/01B_curtain.png`;
    const topCurtain = `${srcBase}/06_rideau_haut.png`;
    const jackpot = `${srcBase}/02_jackpot.png`;
    const up = `${srcBase}/02A_jackpot.png`;
    const down = `${srcBase}/02B_jackpot.png`;
</script>

<div
    class="slot-machine w-full h-full relative overflow-hidden bg-cover bg-no-repeat bg-center"
    on:click={onClick}
    on:keydown={onClick}
>
    {#if $game.bgIngame}
        <img src={$game.bgIngame} alt="bg" class="fixed h-full w-full" />
    {:else}
        <img src={ground} alt="bg" class="fixed bottom-0 w-full h-24" />
        <img src={curtain} alt="bg" class="fixed -top-10 h-full w-full" />
        <img src={topCurtain} alt="bg" class="fixed top-0 w-full h-1/4" />
    {/if}

    {#if showPrice}
        {#if $winner.state === "won"}
            <div class="confetti">
                <Confetti
                    x={[-5, 10]}
                    y={[0, 0.1]}
                    delay={[500, 2000]}
                    duration={5000}
                    amount={400}
                    fallDistance="100vh"
                />
            </div>
            {#if winnerPrice}
                <!-- WON -->
                {#each winnerPrice.tradPacks as word}
                    {#if word.lang === lang}
                        <div
                            in:fly={{ y: -100, delay: 900 }}
                            style="z-index: 11;"
                        >
                            <img
                                src={winnerPrice.img}
                                alt="cadeaux Slot machine"
                                class="relative mx-auto text-center w-96 h-96 mt-32"
                            />
                            <div
                                class="relative mx-auto text-center text-white text-7xl"
                            >
                                {winnerPrice.name}
                            </div>
                        </div>
                    {/if}
                {/each}
            {/if}
        {:else if $winner.state == "lost"}
            <!-- LOST -->
            <div
                in:fly={{ y: -100, delay: 300 }}
                class="relative mt-40 flex items-center justify-center text-white text-9xl"
            >
                {trads.tradDefaults.cross}
            </div>
            <div
                in:fly={{ y: -100, delay: 400 }}
                class="relative flex items-center justify-center text-white text-2xl mt-14"
            >
                {trads.tradDefaults.lost}
            </div>
        {:else if $winner.state == "cant_replay"}
            <!-- CAN REPLAY -->
            <div
                in:fly={{ y: -100, delay: 300 }}
                class="relative mt-40 flex items-center justify-center text-white text-9xl"
            >
                {trads.tradDefaults.cross}
            </div>
            <div
                in:fly={{ y: -100, delay: 400 }}
                class="relative flex items-center justify-center text-white text-2xl mt-14"
            >
                {trads.tradDefaults.cant_replay}
            </div>
        {:else if $winner.state == "cant_replay_today"}
            <!-- CAN REPLAY TODAY-->
            <div
                in:fly={{ y: -100, delay: 300 }}
                class="relative mt-40 flex items-center justify-center text-white text-9xl"
            >
                {trads.tradDefaults.cross}
            </div>
            <div
                in:fly={{ y: -100, delay: 400 }}
                class="relative flex items-center justify-center text-white text-2xl mt-14"
            >
                {trads.tradDefaults.no_more_play_today}
            </div>
        {/if}
    {:else}
        <div
            in:fly={{ y: -100 }}
            out:fly={{ y: 100, delay: 500 }}
            class="jackpot"
        >
            <img
                src={jackpot}
                alt="bg"
                class="absolute overflow-hidden bg-cover bg-no-repeat"
            />
            <div class="reel-wrapper">
                {#each reels as { className, style, price }}
                    <Caption
                        bind:className
                        bind:style
                        bind:price
                        bind:lang
                        {prices}
                        bind:winnerReelsPrice
                    />
                {/each}
            </div>
            {#if stick === "up"}
                <div
                    class="jackpot-stick on"
                    style="background-image: url({up});"
                />
            {:else}
                <div
                    class="jackpot-stick"
                    style="background-image: url({down});"
                />
            {/if}
        </div>
    {/if}
    <!-- reset BTN -->
    {#if readyToRestart && $game.restartBtn && $formSubmited}
        <div
            in:fly={{ y: -100, delay: 500 }}
            on:click={reload}
            on:keypress={reload}
            class=" fixed top-10 right-10 text-white z-20"
        >
            <svg width="4em" height="4em" viewBox="0 0 20 20"
                ><path
                    fill="currentColor"
                    d="M14.66 15.66A8 8 0 1 1 17 10h-2a6 6 0 1 0-1.76 4.24l1.42 1.42zM12 10h8l-4 4l-4-4z"
                /></svg
            >
        </div>
        <!-- END TEXT -->
        {#if trads.tradIntroOutro.closingText && $formSubmited}
            <div
                in:fly={{ y: -100, delay: 300 }}
                class="fixed mx-auto text-center text-white text-3xl bottom-20 center-closing-text"
            >
                {@html trads.tradIntroOutro.closingText}<br />
            </div>
        {/if}
    {/if}
</div>

<style>
    .slot-machine {
        width: 100vw;
        height: 100vh;
    }
    .jackpot {
        background-repeat: no-repeat;
        z-index: 1;
        position: absolute;
        bottom: 10%;
        left: 0;
        right: 0;
        margin: 0 auto;
        height: 615px;
        width: 678px;
        background-size: contain;
    }
    .reel-wrapper {
        background-color: transparent;
        height: 142px;
        width: 445px;
        left: 97px;
        margin: 0;
        position: absolute;
        top: 183px;
        overflow: hidden;
    }
    .jackpot-stick {
        position: absolute;
        width: 41px;
        height: 157px;
        top: 76px;
        right: -7px;
    }
    .jackpot-stick.on {
        position: absolute;
        height: 118px;
        top: 260px;
        right: -10px;
    }
    @media (max-width: 1279px) {
        .jackpot {
            height: 400px;
            width: 525px;
            bottom: 20%;
        }
        .reel-wrapper {
            top: 142px;
            left: 74px;
            width: 348px;
            height: 113px;
        }
        .jackpot-stick {
            top: 23px;
            right: -10px;
        }
        .jackpot-stick.on {
            height: 118px;
            top: 200px;
        }
    }
    @media (max-width: 600px) {
        .jackpot {
            height: 250px;
            width: 320px;
            bottom: 35%;
        }
        .reel-wrapper {
            top: 87px;
            left: 47px;
            width: 209px;
            height: 67px;
        }
        .jackpot-stick {
            background-size: contain;
            width: 25px;
            height: 95px;
            top: 16px;
            right: -7px;
        }
        .jackpot-stick.on {
            height: 72px;
            top: 119px;
        }
    }
    .center-closing-text {
        left: 50%;
        transform: translateX(-50%);
    }
</style>
