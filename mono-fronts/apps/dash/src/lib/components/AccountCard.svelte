<script lang="ts">
    import { RefreshIcon } from "@rgossiaux/svelte-heroicons/solid";
    import { page } from "$app/stores";
    import Tooltip from "./Tooltip.svelte";

    export let emblem: string;
    export let name: string;
    export let type_id: number;
    export let skin_id: number;
    export let type: string;
    export let i: number;

    const src = `https://bearwallet.fra1.cdn.digitaloceanspaces.com/type_n_skins/${type_id}/${skin_id}/thumb.png`;
    let sending = false;

    let errors: string[] = [];
    let warnings: string[] = [];

    (async () => {
        const url = `${$page.url.origin}/validity/${emblem}`;
        const res = await fetch(url);
        const data = await res.json();
        errors = data.errors;
        warnings = data.warnings;
    })();
</script>

<div>
    <a
        on:click|once={() => {
            sending = true;
        }}
        data-sveltekit-preload-data="hover"
        data-test="account-{i}"
        href="/games/{emblem}"
    >
        <div
            class="w-full bg-slate-200 rounded-lg px-6 py-6 shadow-xl hover:scale-110 duration-100"
        >
            {#if !sending}
                <p class="text-5xl text-gray-400 font-bold italic">.0{i + 1}</p>
                <p
                    class="text-lg italic text-gray-700 font-base -mt-3 text-left"
                >
                    {type}
                </p>
                <div class="mb-8">
                    <img
                        class="object-center object-cover rounded-full h-36 w-36 text-center mx-auto my-4"
                        {src}
                        alt="thumb skinned game"
                    />
                </div>
                <div class="text-center">
                    <p class="text-xl text-gray-700 font-bold -mb-1.5">
                        {name}
                    </p>
                    <p class="text-sm text-gray-400 font-semithin mb-2 italic">
                        -{emblem}-
                    </p>
                </div>
            {:else}
                <div class="relative">
                    <div class="opacity-20">
                        <p class="text-5xl text-gray-400 font-bold italic">
                            .0{i + 1}
                        </p>
                        <p
                            class="text-lg italic text-gray-700 font-base -mt-3 text-left"
                        >
                            {type}
                        </p>
                        <div class="mb-8">
                            <img
                                class="object-center object-cover rounded-full h-36 w-36 text-center mx-auto my-4"
                                {src}
                                alt="thumb skinned game"
                            />
                        </div>
                        <div class="text-center">
                            <p class="text-xl text-gray-700 font-bold -mb-1.5">
                                {name}
                            </p>
                            <p
                                class="text-sm text-gray-400 font-semithin mb-2 italic"
                            >
                                -{emblem}-
                            </p>
                        </div>
                    </div>
                    <div class="absolute w-full h-full top-1/3">
                        <div class="text-center mx-auto w-1/2 h-1/2">
                            <RefreshIcon
                                class="rotate-360 animate-spin opacity-75"
                            />
                        </div>
                    </div>
                </div>
            {/if}
            <div class="grid grid-cols-2 gap-4">
                <div class="text-center">
                    {#if errors.length > 0}
                        <Tooltip tooltip={errors.join(", ")}>
                            <span
                                class="bg-red-600 text-white px-2 py-1 rounded-lg text-xs italic mt-10"
                            >
                                Errors!
                            </span>
                        </Tooltip>
                    {/if}
                </div>
                <div class="text-center">
                    {#if warnings.length > 0}
                        <Tooltip tooltip={warnings.join(", ")}>
                            <span
                                class="bg-orange-500 text-white px-2 py-1 rounded-lg text-xs italic mt-10"
                            >
                                Warning!
                            </span></Tooltip
                        >
                    {/if}
                </div>
            </div>
        </div>
    </a>
</div>

<svelte:head>
    <style>
        /*This would all go into the global.css file*/
        [data-tooltip] {
            position: relative;
            z-index: 2;
            display: block;
        }

        [data-tooltip]:before,
        [data-tooltip]:after {
            visibility: hidden;
            opacity: 0;
            pointer-events: none;
            transition: 0.2s ease-out;
            transform: translate(-50%, 5px);
        }

        [data-tooltip]:before {
            position: absolute;
            bottom: 100%;
            left: 50%;
            margin-bottom: 5px;
            padding: 7px;
            width: 200%;
            min-width: 70px;
            max-width: 250px;
            -webkit-border-radius: 3px;
            -moz-border-radius: 3px;
            border-radius: 3px;
            background-color: #000;
            background-color: hsla(0, 0%, 20%, 0.9);
            color: #fff;
            content: attr(data-tooltip);
            text-align: center;
            font-size: 14px;
            line-height: 1.2;
            transition: 0.2s ease-out;
        }

        [data-tooltip]:after {
            position: absolute;
            bottom: 100%;
            left: 50%;
            width: 0;
            border-top: 5px solid #000;
            border-top: 5px solid hsla(0, 0%, 20%, 0.9);
            border-right: 5px solid transparent;
            border-left: 5px solid transparent;
            content: " ";
            font-size: 0;
            line-height: 0;
        }

        [data-tooltip]:hover:before,
        [data-tooltip]:hover:after {
            visibility: visible;
            opacity: 1;
            transform: translate(-50%, 0);
        }
        [data-tooltip="false"]:hover:before,
        [data-tooltip="false"]:hover:after {
            visibility: hidden;
            opacity: 0;
        }
    </style>
</svelte:head>
