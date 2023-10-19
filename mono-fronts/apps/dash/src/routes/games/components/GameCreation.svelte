<script lang="ts">
    import Jar from "./subcomps/Jar.svelte";
    import { enhance } from "$app/forms";
    import { goto } from "$app/navigation";
    import { emblem } from "$lib/stores/index";
    import { page } from "$app/stores";
    import type { TypesNskins, GameType, Skin } from "$lib/types";

    export let typesNskins: TypesNskins;
    let name = "";
    let gameType = "";
    // let skin = "";
    // let backgroundUrl = "";

    const traduction = $page.data.user.traduction;
    const types: GameType[] = typesNskins.types;
    const skinsBase: Skin[] = typesNskins.skins;
    let idSelected = 0;
    let skins: Skin[] = [];
    let idType = 1;
    let idSkin = 1;
    updateSkins(idType);
    updateSkins2(idSkin);
    if (gameType) {
        const gamess = types.filter((x) => x.name === gameType);
        skins = skinsBase.filter((x) => x.game === gamess[0].id);
    } else {
        skins = skinsBase.filter((x) => x.game === idSelected);
    }
    $: src = `https://bearwallet.fra1.cdn.digitaloceanspaces.com/type_n_skins/${idType}/${idSkin}/thumb.png`;

    const checkName = () => {
        if (name && idSkin && idType) {
            redayToCreate = true;
        }
    };

    function updateSkins(ref_id: number): void {
        idType = ref_id;
        idSkin = 1;
        const newTypes = types.find((e) => e.ref_id == idType);
        skins = skinsBase.filter((x) => x.game === newTypes?.id);

        if (name && idSkin && idType) {
            redayToCreate = true;
        }
    }

    function updateSkins2(ref_id: number): void {
        idSkin = ref_id;
        if (name && idSkin && idType) {
            redayToCreate = true;
        }
    }

    const action = "?/create";
    let redayToCreate = false;

    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";
</script>

<svelte:head>
    <title>{traduction.title_game_basics}</title>
</svelte:head>
<section class="bg-white rounded-lg py-12 px-10 font-bold italic shadow-lg">
    {traduction.game_game_creation}
    <form
        class="text-center"
        enctype="multipart/form-data"
        method="POST"
        {action}
        use:enhance={({ form }) => {
            submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
            submitColor = "bleu-gris/[.3]";
            cursor = "cursor-not-allowed";
            return async ({ result }) => {
                goto(`/games/${result.data.emblem}`);
            };
        }}
    >
        <input type="hidden" name="emblem" value={$emblem} />
        <input type="hidden" name="gameType" value={idType} />
        <input type="hidden" name="skin" value={idSkin} />
        <div
            class="w-full mx-auto text-center flex items-center justify-center"
        >
            <div class="group my-10">
                <label for="name" class="label"
                    >{traduction.game_name}:
                    <input
                        on:blur={checkName}
                        data-test="name"
                        type="text"
                        name="name"
                        class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                        required
                        bind:value={name}
                    />
                </label>
            </div>
        </div>
        <div class="flex">
            <div class="w-1/2">
                <Jar
                    listOf={types}
                    title={traduction.game_section}
                    bind:id={idType}
                    updateFunction={updateSkins}
                />
                <Jar
                    listOf={skins}
                    title={traduction.game_selection_theme}
                    bind:id={idSkin}
                    updateFunction={updateSkins2}
                />
            </div>
            <div class=" text-center mx-auto">
                <img {src} alt="game ribbon" class="m-10 w-96 rounded-lg" />
            </div>
        </div>
        <div class="bg-bleu-gris" />
        <div class="bg-bleu-gris/[.3]" />
        {#if redayToCreate}
            <div class="bg-bleu-swapye-1" />
            <button
                type="submit"
                class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
                data-test="submit"
            >
                <p class="text-center mx-auto">
                    {@html submitText}
                </p>
            </button>
        {:else}
            <button
                type="submit"
                class="px-10 py-2 text-white bg-gray-500 rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-gray-500/50 font-bold cursor-not-allowed"
                disabled
            >
                <p class="text-center mx-auto">
                    {@html submitText}
                </p>
            </button>
        {/if}
    </form>
</section>

<style>
    :global(.checked) {
        @apply bg-bleu-gris  text-white relative rounded-lg shadow-md h-10 cursor-pointer flex focus:outline-none w-full items-center;
    }
</style>
