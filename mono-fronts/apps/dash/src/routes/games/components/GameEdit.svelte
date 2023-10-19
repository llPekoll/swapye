<script lang="ts">
    import Jar from "./subcomps/Jar.svelte";
    import { enhance } from "$app/forms";
    import { emblem } from "$lib/stores";
    import type { TypesNskins, GameType, Skin, Basics } from "$lib/types";
    import DropZone from "$lib/components/DropZone.svelte";
    import { page } from "$app/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";
    import { basics as basicsStore } from "$lib/stores";

    const typesNskins: TypesNskins = $page.data.user.typesNskins;
    const traduction = $page.data.user.traduction;
    const types: GameType[] = typesNskins.types;
    const skinsBase: Skin[] = typesNskins.skins;
    const basics: Basics = $basicsStore;
    let skins: Skin[] = [];
    let name = basics.name as string;
    let idType = basics.type;
    let idSkin = basics.skin;
    let bgIngame = basics.bgIngame;
    console.log(bgIngame);
    updateSkins(idType);
    updateSkins2(idSkin);

    function updateSkins(ref_id: number): void {
        idType = ref_id;
        const newTypes = types.find((e) => e.ref_id == idType);
        skins = skinsBase.filter((x) => x.game === newTypes?.id);
        idSkin = 1;
    }
    function updateSkins2(ref_id: number): void {
        idSkin = ref_id;
    }

    let cleared = false;
    const clearUrl = `/perso/${$emblem}/clear/bgingame`;
    $: if (cleared) {
        basicsStore.update((base) => {
            base.bgIngame = "";
            base.idSkin = idSkin;
            base.idType = idType;
            base.name = name;
            return base
            });
    }
    $: src = `https://bearwallet.fra1.cdn.digitaloceanspaces.com/type_n_skins/${idType}/${idSkin}/thumb.png`;
    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let needsUpdate = false;
    let disabled = true;
    $: if (needsUpdate) {
        submitText = traduction.submit;
        submitColor = "bleu-gris";
        cursor = "cursor-pointer";
        disabled = false;
    } else {
        submitText = traduction.submit;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        disabled = true;
    }
</script>

<svelte:head>
    <title>{traduction.title_game_basics}</title>
</svelte:head>
<section class="p-10">
    <img src="/basics2.svg" class="text-center w-44 inline" alt="basics" />
    <p class="align-bottom inline text-5xl font-bold italic text-slate-400">
        {traduction.title_game_basics}
    </p>
    <form
        class="text-center"
        enctype="multipart/form-data"
        method="POST"
        action="?/basics"
        use:enhance={() => {
            submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
            submitColor = "bleu-gris/[.3]";
            cursor = "cursor-not-allowed";
            return async ({ result }) => {
                if (result.type === "success") {
                    console.log("result.data");
                    console.log(result.data);
                    $basicsStore.name = result.data?.name;
                    $basicsStore.idSkin = result.data?.skin;
                    $basicsStore.idType = result.data?.type;
                    $basicsStore.bgIngame = result.data?.bgIngame;
                    toast.push(traduction.toast_success, { ...successToast });
                } else {
                    toast.push(
                        `${traduction.toast_error}, ${result.error.message}`,
                        {
                            ...errorToast,
                        }
                    );
                }
                needsUpdate = false;
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
                        on:blur={() => (needsUpdate = true)}
                        data-test="name"
                        type="text"
                        name="name"
                        class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                        required
                        value={name}
                    />
                </label>
            </div>
        </div>
        <div class="flex">
            <div
                class="w-1/2"
                on:click={() => (needsUpdate = true)}
                on:keypress={() => (needsUpdate = true)}
            >
                <Jar
                    listOf={types}
                    title={traduction.game_section}
                    bind:id={idType}
                    updateFunction={updateSkins}
                />
                {#if !bgIngame}
                    <Jar
                        listOf={skins}
                        title={traduction.game_selection_theme}
                        bind:id={idSkin}
                        updateFunction={updateSkins2}
                    />
                {:else}
                    <input name="idSkin" value="1" type="hidden" />
                {/if}
            </div>
            <div class=" text-center mx-auto">
                <img {src} alt="game ribbon" class="m-10 w-96 rounded-lg" />
            </div>
        </div>
        <div class="bg-bleu-gris" />
        <div class="bg-bleu-gris/[.3]" />

        <p class="text-center text-3xl font-bold text-slate-800 py-5">
            Image de fond
        </p>
        <div on:change={() => (needsUpdate = true)}>
            <DropZone
                fileType="image"
                name="bgIngame"
                src={bgIngame}
                {clearUrl}
                bind:cleared
                whatItisToUpload="fond d'écran du jeux"
            />
        </div>
        <button
            type="submit"
            class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-10 shadow-lg shadow-{submitColor} font-bold {cursor}"
            {disabled}
        >
            <p class="text-center mx-auto">
                {@html submitText}
            </p>
        </button>
    </form>
</section>

<style>
    :global(.checked) {
        @apply bg-bleu-gris  text-white relative rounded-lg shadow-md h-10 cursor-pointer flex w-full items-center focus:outline-none;
    }
</style>
