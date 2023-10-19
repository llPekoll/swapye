<script lang="ts">
    import type {
        TradDefaults,
        TradIntroOutro,
        TradPrices,
    } from "$lib/interfaces";
    import Telephone from "$lib/components/FormInputs/Telephone.svelte";
    import { fly } from "svelte/transition";
    import { page } from "$app/stores";
    import Loading from "$lib/components/Loading.svelte";
    import { enhance } from "$app/forms";
    import { toast } from "@zerodevx/svelte-toast";
    import { game, winner, formSubmited } from "$lib/stores";
    import type { E164Number } from "svelte-tel-input/types";

    export let lang = "fr";
    export let trads: {
        tradDefaults: TradDefaults;
        tradIntroOutro: TradIntroOutro;
        tradPrices: TradPrices[];
        langs: string[];
    };
    export let fullScreenSwitcher: () => void;

    const extraReqElts = $game.extraRequested;

    let emailCheckState = "idle";
    if (!$game.emailCheck) {
        emailCheckState = "valid";
    }
    // TODO regarder si le compte demande un check ou pas!!!!!!!!!!!!!
    let id: number; // id of the mailcheck
    // const delay = (ms:number) => new Promise((res) => setTimeout(res, ms));
    const checkEmail = async (event: FocusEvent) => {
        console.log("emailCheckState 1", emailCheckState);
        if ($game.dryRun) {
            emailCheckState = "valid";
            return true;
        }
        console.log("emailCheckState 2", emailCheckState);
        const v = event.target as HTMLInputElement;
        let email: string;
        email = v.value;
        console.log(email);
        const re = /\S+@\S+\.\S+/;
        if (!re.test(email as unknown as string)) {
            return false;
        }
        console.log("emailCheckState 3", emailCheckState);
        emailCheckState = "loading";

        // ========== PRODUCTION
        const ret = await fetch(`${$page.url.origin}/email_validate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, emblem: $game.emblem }),
        });
        console.log("emailCheckState 4", emailCheckState);
        const data = await ret.json();
        if (data.status === "valid") {
            emailCheckState = "valid";
            id = data.id;
            console.log("id", id);
        } else {
            emailCheckState = "wrong";
        }
        console.log("emailCheckState", emailCheckState);
        // ========== PRODUCTION

        // ==========DEBUG ONLY
        // await delay(50000);

        // emailCheckState = "valid";
        // ==========DEBUG ONLY
        return;
    };

    let phone: E164Number | null = null;
    let submitted = false;
</script>

<div
    out:fly={{ y: -100 }}
    class="relative menu flex items-center justify-center w-screen h-screen scrollbar-thin scrollbar-thumb-slate-800 scrollbar-track-transparent overflow-y-scroll"
>
    {#if $game.displayFullScreen && $game.fullscreenBtn}
        <div
            class="text-white absolute top-10 left-10 md:block hidden"
            on:click={fullScreenSwitcher}
            on:keypress={fullScreenSwitcher}
        >
            <svg width="4em" height="4em" viewBox="0 0 24 24">
                <g fill="none">
                    <path d="M24 0H0v24h24z" />
                    <path
                        fill="currentColor"
                        d="M18.5 5.5H16a1.5 1.5 0 0 1 0-3h3A2.5 2.5 0 0 1 21.5 5v3a1.5 1.5 0 0 1-3 0V5.5ZM8 5.5H5.5V8a1.5 1.5 0 1 1-3 0V5A2.5 2.5 0 0 1 5 2.5h3a1.5 1.5 0 1 1 0 3Zm0 13H5.5V16a1.5 1.5 0 0 0-3 0v3A2.5 2.5 0 0 0 5 21.5h3a1.5 1.5 0 0 0 0-3Zm8 0h2.5V16a1.5 1.5 0 0 1 3 0v3a2.5 2.5 0 0 1-2.5 2.5h-3a1.5 1.5 0 0 1 0-3Z"
                    />
                </g>
            </svg>
        </div>
    {/if}
    <form
        method="post"
        action="?/postgameform"
        class=" backdrop-blur bg-black/30 md:px-20 px-2 max-w-xl py-10 rounded-lg"
        use:enhance={({ form }) => {
            submitted = true;
            return async ({ result, update }) => {
                console.log(
                    "!!!!!!!!!!!!!!!!return from form!!!!1!!!!!!!!",
                    result
                );
                if (result.type === "success") {
                    if (result.data?.price) {
                        const id = result.data?.price;
                        const priceWon = trads.tradPrices.filter(
                            (trad) => trad.priceId == id
                        )[0];
                        console.log(
                            "==============priceWon ===============",
                            priceWon
                        );
                        console.log("trad", trads);
                        console.log("priceWon", priceWon);
                        winner.set({
                            price: id,
                            state: result.data?.state,
                            img: priceWon.img,
                            name: priceWon.name,
                            displayTitle: result.data?.displayTitle,
                            offsetTitle: result.data?.offsetTitle,
                            dayNumber: result.data?.dayNumber,
                        });
                    } else {
                        winner.set({
                            state: result.data?.state,
                            dayNumber: result.data?.dayNumber,
                        });
                    }
                    formSubmited.set(true);
                }
                if (result.type === "error") {
                    toast.push(`error, ${result.error.message}`, {
                        theme: {
                            "--toastColor": "black",
                            "--toastBackground": "white",
                            "--toastBarBackground": "red",
                        },
                    });
                }
                form.reset();
                await update();
                submitted = false;
            };
        }}
    >
        <input type="hidden" name="emblem" value={$game.emblem} />
        <input type="hidden" name="validation_id" value={id} />
        {#if $game.dryRun}
            <div
                class="text-red-500 font-bold text-3xl text-center animate-bounce"
            >
                [TEST MODE]
            </div>
        {/if}
        <!-- {#if loaded}
            <img
                on:error={() => (loaded = false)}
                src="fasdfasdf"
                alt="logo"
                class="max-w-20 max-h-20 mx-auto"
            />
        {/if} -->
        {#if $game.logo}
            <img
                src={$game.logo}
                class="max-w-20 max-h-20 mx-auto"
                alt="logo"
            />
        {/if}
        <!-- <BgElement
            className="max-w-20 max-h-20 mx-auto"
            alt="Logo"
            src={logo}
        /> -->
        {#if trads.tradIntroOutro.openingText}
            <p class="text-white mx-auto text-center py-4">
                {@html trads.tradIntroOutro.openingText}
            </p>
        {:else}
            <h1
                class="font-thin uppercase my-4 tracking-wide mx-auto text-center text-white"
            >
                {$game.name}
            </h1>
        {/if}
        {#if $game.requestName}
            <div class="question" style="--theme-color: {$game.formColor}">
                <input
                    type="text"
                    required
                    name="name"
                    value=""
                    autocomplete="off"
                />
                <label for="name">{trads.tradDefaults.name}</label>
            </div>
        {/if}
        <div class="question" style="--theme-color: {$game.formColor}">
            {#if $game.emailCheck}
                <input
                    on:blur={checkEmail}
                    type="email"
                    required
                    name="email"
                    value=""
                    autocomplete="off"
                />
            {:else}
                <input
                    type="email"
                    required
                    name="email"
                    value=""
                    autocomplete="off"
                />
            {/if}
            <label for="email">{trads.tradDefaults.email}</label>
        </div>
        {#if $game.emailCheck}
            {#if emailCheckState === "loading"}
                <div class="flex justify-center text-white text-7xl">
                    <svg width="0.7em" height="0.7em" viewBox="0 0 24 24">
                        <circle cx="18" cy="12" r="0" fill="currentColor"
                            ><animate
                                attributeName="r"
                                begin=".67"
                                calcMode="spline"
                                dur="1.5s"
                                keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8"
                                repeatCount="indefinite"
                                values="0;2;0;0"
                            /></circle
                        ><circle cx="12" cy="12" r="0" fill="currentColor"
                            ><animate
                                attributeName="r"
                                begin=".33"
                                calcMode="spline"
                                dur="1.5s"
                                keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8"
                                repeatCount="indefinite"
                                values="0;2;0;0"
                            /></circle
                        ><circle cx="6" cy="12" r="0" fill="currentColor"
                            ><animate
                                attributeName="r"
                                begin="0"
                                calcMode="spline"
                                dur="1.5s"
                                keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8"
                                repeatCount="indefinite"
                                values="0;2;0;0"
                            /></circle
                        ></svg
                    >
                </div>
            {:else if emailCheckState === "valid"}
                <div class="flex justify-center">
                    <p class="text-green-500">Email valide</p>
                </div>
            {:else if emailCheckState === "wrong"}
                <div class="flex justify-center">
                    <p class="text-red-500">Email invalide</p>
                </div>
            {/if}
        {/if}
        {#if $game.requestTel}
            <div class="" style="--theme-color: {$game.formColor}">
                <label
                    for="phone"
                    class="tel"
                    style="--theme-color: {$game.formColor}"
                    >{trads.tradDefaults.phone}</label
                >
                <input type="hidden" name="phone" value={phone} />
                <Telephone bind:value={phone} />
            </div>
        {/if}
        {#if $game.requestAddress}
            <div class="question" style="--theme-color: {$game.formColor}">
                <input
                    type="text"
                    required
                    autocomplete="off"
                    name="address"
                    value=""
                />
                <label for="adrress">{trads.tradDefaults.address}</label>
            </div>
        {/if}
        {#each extraReqElts as { kind, key, wordings }}
            {#if kind === "Checkbox"}
                <div class="clear-both py-2 pt-10">
                    <label class="toggler-wrapper style-1 float-right">
                        <input type="checkbox" name={key} />
                        <div
                            class="toggler-slider"
                            style="--theme-color: {$game.formColor}"
                        >
                            <div class="toggler-knob" />
                        </div>
                    </label>
                    {#each wordings as word}
                        {#if word.lang == lang}
                            <p class="text-white">{word.wording}</p>
                        {/if}
                    {/each}
                </div>
            {:else}
                {#each wordings as word}
                    {#if word.lang == lang}
                        <div
                            class="question"
                            style="--theme-color: {$game.formColor}"
                        >
                            <input
                                type="text"
                                required
                                autocomplete="off"
                                name={key}
                            />
                            <label for={key}>{word.wording}</label>
                        </div>
                    {/if}
                {/each}
            {/if}
        {/each}

        <div class="clear-both py-2 pt-10">
            <label class="toggler-wrapper style-1 float-right">
                <input type="checkbox" name="requestEmail" />

                <div
                    class="toggler-slider"
                    style="--theme-color: {$game.formColor}"
                >
                    <div class="toggler-knob" />
                </div>
            </label>
            <p class="text-white">{trads.tradDefaults.policy}</p>
        </div>
        <div class="clear-both py-2">
            <label class="toggler-wrapper style-1 float-right">
                <input type="checkbox" name="requestEmail" required />

                <div
                    class="toggler-slider"
                    style="--theme-color: {$game.formColor}"
                >
                    <div class="toggler-knob" />
                </div>
            </label>
            <p class="text-white">{trads.tradDefaults.rules}</p>
        </div>

        {#if emailCheckState == "valid"}
            {#if submitted}
                <div class="container mt-10 flex items-center justify-center">
                    <button
                        id="button"
                        style="--theme-color: {$game.formColor}"
                        class="wrong"
                        disabled
                    >
                        <Loading />
                    </button>
                </div>
            {:else}
                <div class="container mt-10 flex items-center justify-center">
                    <button id="button" style="--theme-color: {$game.formColor}"
                        >{trads.tradDefaults.submit}</button
                    >
                </div>
            {/if}
        {:else}
            <div class="container mt-10 flex items-center justify-center">
                <button id="button" class="wrong" disabled
                    >{trads.tradDefaults.submit}</button
                >
            </div>
        {/if}
    </form>
</div>

<style>
    .menu {
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.75);
    }

    form button,
    form .question label,
    form .question input {
        -moz-transition: all 0.25s cubic-bezier(0.53, 0.01, 0.35, 1.5);
        -o-transition: all 0.25s cubic-bezier(0.53, 0.01, 0.35, 1.5);
        -webkit-transition: all 0.25s cubic-bezier(0.53, 0.01, 0.35, 1.5);
        transition: all 0.25s cubic-bezier(0.53, 0.01, 0.35, 1.5);
    }

    /* Button */
    .tel {
        color: var(--theme-color);
        font-weight: 100;
        letter-spacing: 0.01em;
        font-size: 17px;
    }
    button {
        outline: none;
        height: 40px;
        text-align: center;
        width: 130px;
        border-radius: 40px;
        background: #fff;
        border: 2px solid var(--theme-color);
        color: var(--theme-color);
        letter-spacing: 1px;
        text-shadow: 0;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.25s ease;
    }
    button:hover {
        color: white;
        background: var(--theme-color);
    }
    button:active {
        letter-spacing: 2px;
    }
    .wrong {
        outline: none;
        height: 40px;
        text-align: center;
        width: 130px;
        border-radius: 40px;
        background: #fff;
        border: 2px solid gray;
        color: gray;
        letter-spacing: 1px;
        text-shadow: 0;
        font-size: 12px;
        font-weight: bold;
        cursor: wait;
        transition: all 0.25s ease;
    }
    .wrong:hover {
        color: white;
        background: gray;
    }
    .wrong:active {
        letter-spacing: 2px;
    }

    form .question {
        position: relative;
        padding: 10px 0;
    }
    form .question:first-of-type {
        padding-top: 0;
    }
    form .question:last-of-type {
        padding-bottom: 0;
    }
    form .question label {
        transform-origin: left center;
        color: var(--theme-color);
        font-weight: 100;
        letter-spacing: 0.01em;
        font-size: 17px;
        box-sizing: border-box;
        padding: 10px 15px;
        display: block;
        position: absolute;
        margin-top: -40px;
        z-index: 2;
        pointer-events: none;
    }
    form .question input {
        appearance: none;
        background-color: none;
        border: 1px solid var(--theme-color);
        line-height: 0;
        font-size: 17px;
        width: 100%;
        display: block;
        box-sizing: border-box;
        padding: 10px 15px;
        border-radius: 60px;
        color: var(--theme-color);
        font-weight: 100;
        letter-spacing: 0.01em;
        position: relative;
        z-index: 1;
    }
    form .question input:focus {
        outline: none;
        background: var(--theme-color);
        color: white;
        margin-top: 30px;
    }
    form .question input:valid {
        margin-top: 30px;
    }
    form .question input:focus ~ label {
        -moz-transform: translate(0, -35px);
        -ms-transform: translate(0, -35px);
        -webkit-transform: translate(0, -35px);
        transform: translate(0, -35px);
    }
    form .question input:valid ~ label {
        text-transform: uppercase;
        font-style: italic;
        -moz-transform: translate(5px, -35px) scale(0.6);
        -ms-transform: translate(5px, -35px) scale(0.6);
        -webkit-transform: translate(5px, -35px) scale(0.6);
        transform: translate(5px, -35px) scale(0.6);
    }

    /* second css */

    input[type="checkbox"] {
        position: absolute;
        opacity: 0;
        z-index: -1;
    }

    .toggler-wrapper.style-1
        input[type="checkbox"]:checked
        + .toggler-slider
        .toggler-knob {
        left: calc(100% - 19px - 3px);
    }

    .toggler-wrapper.style-1 .toggler-knob {
        width: calc(25px - 6px);
        height: calc(25px - 6px);
        border-radius: 50%;
        left: 3px;
        top: 3px;
        background-color: #fff;
    }
    .toggler-wrapper {
        display: block;
        width: 45px;
        height: 25px;
        cursor: pointer;
        position: relative;
    }

    .toggler-wrapper input[type="checkbox"]:checked + .toggler-slider {
        background-color: var(--theme-color);
    }

    .toggler-wrapper .toggler-slider {
        background-color: #ccc;
        position: absolute;
        border-radius: 100px;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        -webkit-transition: all 300ms ease;
        transition: all 300ms ease;
    }

    .toggler-wrapper .toggler-knob {
        position: absolute;
        -webkit-transition: all 300ms ease;
        transition: all 300ms ease;
    }
</style>
