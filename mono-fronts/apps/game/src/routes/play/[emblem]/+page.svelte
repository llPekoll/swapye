<script lang="ts">
    import { fly, fade } from "svelte/transition";
    import type { Trads, Winner } from "$lib/interfaces";
    import type { PageData } from "./$types";
    import Curtain from "$lib/components/games/curtain/Curtain.svelte";
    import Calendar from "$lib/components/games/calendar/Calendar.svelte";
    import SlotMachine from "$lib/components/games/slotMachine/SlotMachine.svelte";
    import Scratch from "$lib/components/games/scratch/Scratch.svelte";
    import SlingShot from "$lib/components/games/slingshot/SlingShot.svelte";
    import Form from "$lib/components/Form.svelte";
    import { onMount } from "svelte";
    import LangSelector from "$lib/components/LangSelector.svelte";

    import { game, winner, formSubmited } from "$lib/stores";

    export let data: PageData;
    const tractuctions: Trads = data.trads;
    const langs: string[] = data.langs;
    console.log("data.prices");
    console.log(data.prices);
    const prices = data.prices;

    game.set(data.game);
    let lang = langs[0] as
        | "🇫🇷 France"
        | "🇬🇧 Anglais"
        | "🇪🇸 Espagnol"
        | "🇮🇹 Italien"
        | "🇩🇪 Allemand"
        | "🇨🇳 Chinois";

    $: trads = tractuctions[lang];
    let state = "idle";

    //  Image intro smartphone or not
    let h: number = 0;
    let w: number = 0;
    let isSmartphone: boolean = false;
    let hiddeIntro = false;

    $: if (h > w) {
        isSmartphone = true;
    } else {
        isSmartphone = false;
    }

    let fail = false;
    let reload: () => void;

    const fullScreenSwitcher = () => {
        $game.displayFullScreen = false;
        // Supports most browsers and their versions.
        const elem = document.body as HTMLBodyElement;
        var requestMethod =
            elem.requestFullScreen ||
            elem.webkitRequestFullScreen ||
            elem.mozRequestFullScreen ||
            elem.msRequestFullScreen;

        if (requestMethod) {
            // Native full screen.
            requestMethod.call(elem);
        } else if (typeof window.ActiveXObject !== "undefined") {
            // Older IE.
            var wscript = new ActiveXObject("WScript.Shell");
            if (wscript !== null) {
                wscript.SendKeys("{F11}");
            }
        }
    };

    reload = () => {
        winner.set({
            price: 0,
            state: "lost",
            img: "",
            name: "",
            displayTitle: false,
            offsetTitle: "",
        });
        formSubmited.set(false);
        hiddeIntro = false;
    };
    onMount(() => {
        if (document.addEventListener) {
            document.addEventListener("fullscreenchange", exitHandler, false);
            document.addEventListener(
                "mozfullscreenchange",
                exitHandler,
                false
            );
            document.addEventListener("MSFullscreenChange", exitHandler, false);
            document.addEventListener(
                "webkitfullscreenchange",
                exitHandler,
                false
            );
        }

        function exitHandler() {
            if (
                !document.webkitIsFullScreen &&
                !document.mozFullScreen &&
                !document.msFullscreenElement
            ) {
                displayFullScreen = true;
            }
        }
    });

    const reloadSlot = () => {
        winner.set({} as Winner);
        trads[1] = tractuctions[lang][1];
        formSubmited.set(false);
        hiddeIntro = false;
        state = "idle";
    };
    formSubmited.set(false);
    console.log($formSubmited);
    const srcBase = `https://bearwallet.fra1.cdn.digitaloceanspaces.com/type_n_skins/${$game.gameTypeIdRef}/${$game.skinIdRef}`;
</script>

<svelte:head>
    <title>{$game.name}</title>
</svelte:head>

<svelte:window bind:innerHeight={h} bind:innerWidth={w} />

{#if $game.gameTypeIdRef == 1}
    <Curtain {trads} {reload} {srcBase} />
{:else if $game.gameTypeIdRef == 2}
    <Calendar
        ndDays={$game.numberOfDays}
        winnerDay={$game.winnerDay}
        {trads}
        {srcBase}
    />
{:else if $game.gameTypeIdRef == 3}
    <SlotMachine bind:state {prices} {lang} {trads} {reloadSlot} {srcBase} />
{:else if $game.gameTypeIdRef == 4}
    <Scratch {trads} {reload} {srcBase} />
{:else if $game.gameTypeIdRef == 5}
    <SlingShot {trads} {reload} {srcBase} />
{/if}

{#if !$formSubmited}
    <section
        out:fly={{ y: -100 }}
        class="fixed top-0 left-0 w-full h-full z-10"
    >
        {#if fail}
            <p>Error while sending data</p>
        {/if}
        <Form bind:lang {trads} {fullScreenSwitcher} />
        <LangSelector bind:lang {langs} />
    </section>
    {#if $game.formPortrait && isSmartphone && !hiddeIntro}
        <button
            class="fixed top-0 right-0 z-10 h-screen w-screen"
            on:click={() => (hiddeIntro = true)}
            on:keypress={() => (hiddeIntro = true)}
            out:fade
        >
            <img
                src={$game.formPortrait}
                alt="portrait"
                class="h-full w-full"
            />
        </button>
    {/if}
    {#if $game.formLandscape && !isSmartphone && !hiddeIntro}
        <button
            class="fixed top-0 right-0 z-10 h-screen w-screen"
            on:click={() => (hiddeIntro = true)}
            on:keypress={() => (hiddeIntro = true)}
            out:fade
        >
            <img
                src={$game.formLandscape}
                alt="landscape"
                class="h-full w-full"
            />
        </button>
    {/if}
{/if}
{#if $game.music}
    <audio autoplay loop>
        <source src={$game.music} />
    </audio>
{/if}

<style>
    audio {
        display: none;
    }
</style>
