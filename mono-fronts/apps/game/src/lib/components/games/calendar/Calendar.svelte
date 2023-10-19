<script lang="ts">
    import type {
        TradDefaults,
        TradIntroOutro,
        TradPrices,
    } from "$lib/interfaces";
    import { game, formSubmited, winner } from "$lib/stores";
    import { fly } from "svelte/transition";
    import Door from "./Door.svelte";
    import BgElement from "$lib/components/BgElement.svelte";
    export let ndDays: number[] = [];
    export let winnerDay: 1;
    export let trads: {
        tradDefaults: TradDefaults;
        tradIntroOutro: TradIntroOutro;
        tradPrices: TradPrices;
        langs: string[];
    };
    export let srcBase = "";

    let modaleOn = false;
    let submitModale = false;

    const bg = `${srcBase}/01_Fond.jpg`;
    const rubanBas = `${srcBase}/02_Ruban_bas.png`;
    const rubanHaut = `${srcBase}/03_Ruban_haut.png`;
    const loupiotes = `${srcBase}/04_Lupiotes.png`;
    const cadre = `${srcBase}/05_Cadre.png`;
    const bandeGauche = `${srcBase}/06_Bande_gauche.png`;
    const bandeBas = `${srcBase}/07_Bande_bas.png`;
    const bandeHaut = `${srcBase}/08_Bande_haut.png`;
    const bandeDroite = `${srcBase}/09_Bande_droite.png`;
    const vignette = `${srcBase}/10_Vignettage.png`;
    const bulle = `${srcBase}/12_Bulle.png`;
    const logo_har = `${srcBase}/logo_harcour.png`;
    const harcour_fr = `${srcBase}/phrase_VF.png`;
    console.log("winnerDay ->", ndDays);
    const objDoors = ndDays.map((x, i) => {
        return {
            dayNb: x,
            doorImg: `${srcBase}/11_Calendrier_${ndDays[i]
                .toString()
                .padStart(2, "0")}.png`,
            is_winner: x == winnerDay,
        };
    });
    $: if (submitModale) {
        modaleOn = true;
    }
</script>

<div class="relative h-full">
    {#if $game.bgIngame}
        <BgElement
            className="fixed w-full h-full"
            alt="Logo"
            src={$game.bgIngame}
        />
    {:else}
        <BgElement className="fixed w-full h-full top-0" alt="bg" src={bg} />
    {/if}
    <BgElement
        className="fixed bottom-0 w-full"
        alt="rubanBas"
        src={rubanBas}
    />
    <BgElement
        className="fixed bottom-0 left-0 "
        alt="bandebas"
        src={bandeBas}
    />

    <div
        class="{$game.skinIdRef == 2
            ? 'mt-32 md:mt-64 px-0.5 md:px-32'
            : 'mt-20  px-20'} mx-0 absolute my-20 py-12 flex flex-wrap justify-center top-100 overflow-hidden"
        style={!$formSubmited ? "position:fixed;" : ""}
    >
        {#each objDoors as { dayNb, doorImg, is_winner }}
            <Door
                bind:submitModale
                {is_winner}
                src={doorImg}
                {dayNb}
                skin={$game.skinIdRef}
            />
        {/each}
    </div>
    {#if $game.skinIdRef == 2}
        <img src="/mask.png" alt="bulle" class="fixed w-full h-full" />
    {/if}
    <BgElement className="fixed top-0 w-full h-full" alt="cadre" src={cadre} />
    <BgElement
        className="fixed left-0 h-full"
        alt="bandeGauche"
        src={bandeGauche}
    />

    {#if $game.skinIdRef == 2}
        <img src={bandeHaut} alt="bulle" class="fixed top-0 right-0" />
    {/if}
    <BgElement
        className="fixed top-0 right-0"
        alt="bandeHaut"
        src={bandeHaut}
    />
    <BgElement
        className="fixed right-0 h-full"
        alt="rubanHaut"
        src={bandeDroite}
    />
    <BgElement className="fixed top-0 w-full" alt="rubanHaut" src={rubanHaut} />
    {#if $game.skinIdRef !== 2}
        <BgElement
            className="fixed w-full h-full"
            alt="vignette"
            src={vignette}
        />
        <BgElement
            className="fixed top-0 w-full h-full"
            alt="loupiotes"
            src={loupiotes}
        />
    {/if}

    {#if $game.skinIdRef == 2}
        <img
            src={logo_har}
            alt="bulle"
            class="fixed w-96 vv text-center mx-auto top-16 hh"
        />
        <img src={harcour_fr} alt="bulle" class="fixed w-96 vv top-32 hh" />
    {/if}
</div>
{#if modaleOn}
    {#if $game.skinIdRef == 2}
        {#if $winner.state == "cant_replay_today"}
            <div class="fixed h-full w-full bg-black bg-opacity-80">
                <div in:fly={{ y: -100, duration: 400 }} class="relative jj">
                    <img
                        src="https://bearwallet.fra1.digitaloceanspaces.com/dev/logos/1669912727.jpg"
                        alt="lost"
                        class="absolute w-96 vv"
                    />
                </div>
            </div>
        {:else}
            <div class="fixed h-full w-full bg-black bg-opacity-80">
                <div in:fly={{ y: -100, duration: 400 }} class="relative jj">
                    <img src={$winner.img} alt="won" class="absolute w-96 vv" />
                </div>
            </div>
        {/if}
    {:else}
        <div class="fixed h-full w-full bg-black bg-opacity-80">
            <div in:fly={{ y: -100, duration: 400 }} class="relative jj">
                <img src={bulle} alt="bulle" class="absolute w-96 vv" />
                <div
                    class="absolute text-4xl font-semibold text-white vv text-center"
                >
                    {#if $winner.img}
                        <img
                            src={$winner.img}
                            alt="price"
                            class="text-center mx-auto jism"
                        />
                    {:else}
                        <p class=" text-center mx-auto">❌</p>
                    {/if}
                    {#if $winner.state !== "lost" && $winner.displayTitle}
                        {#if $winner.name}
                            <p class="pt-4">{$winner.name}</p>
                        {/if}
                    {/if}
                    {#if $winner.state == "lost"}
                        <p class="pt-4">{trads.tradDefaults.lost}</p>
                    {/if}
                    {#if trads.tradIntroOutro.closingText && !$formSubmited}
                        <p class="text-sm">
                            {@html trads.tradIntroOutro.closingText}
                        </p>
                    {/if}
                </div>
            </div>
        </div>
    {/if}
{/if}

<style>
    img {
        pointer-events: none;
    }
    .jj {
        left: 50%;
        top: 50%;
    }
    .vv {
        transform: translate(-50%, -50%);
    }
    .hh {
        left: 50%;
    }
    .jism {
        max-width: 18rem;
        max-height: 11rem;
    }
</style>
