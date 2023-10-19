<script lang="ts">
    import { enhance } from "$app/forms";
    import { emblem, identity as id } from "$lib/stores/index";
    import { page } from "$app/stores";
    import DropZone from "$lib/components/DropZone.svelte";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";

    const traduction = $page.data.user.traduction;
    let langs = $id.langs;
    let color = ($id.color ? $id.color : "#3d516d") as string;
    let openingText = $id.openingText === undefined ? $id.openingText : "";

    let cleared = false;
    const clearUrl = `/perso/clear/${$emblem}/logo`;

    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";

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

<form
    class="w-full px-10 pt-10"
    enctype="multipart/form-data"
    method="POST"
    action="?/identity"
    use:enhance={({ form }) => {
        submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        return async ({ result, update }) => {
            if (result.type === "success") {
                $id.logoCompnay = result.data?.logoCompnay;
                $id.openingText = result.data?.openingText;
                $id.closingText = result.data?.closingText;
                $id.color = result.data?.color;
                $id.langs = result.data?.langs;

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
    <DropZone
        fileType="image"
        name="logo"
        src={$id.logoCompnay}
        {clearUrl}
        bind:cleared
        whatItisToUpload="Logo"
        bind:needsUpdate
    />
    <div class="flex justify-center items-center mx-auto py-5 w-full" />
    {#if openingText}
        <label for="startText" class="text-slate-600">
            {traduction.logo_starttext}<br />
            <input
                on:blur={() => (needsUpdate = true)}
                type="text"
                name="startText"
                class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                value={$id.openingText}
            />
        </label>
    {:else}
        {#each langs as lang}
            <div class="inline">
                <label for="endText" class="text-slate-600"
                    >{traduction.logo_starttext}
                    <span class="text-xs">{lang.lang} </span>
                    <input
                        on:blur={() => (needsUpdate = true)}
                        type="text"
                        name="opening_text_{lang.lang}"
                        class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                        value={lang.openingText}
                    />
                </label>
            </div>
        {/each}
    {/if}
    {#if $id.closingText}
        <label for="endText" class="text-slate-600">
            {traduction.logo_endtext}<br />
            <input
                on:blur={() => (needsUpdate = true)}
                type="text"
                name="endText"
                class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                value={$id.closingText ? $id.closingText : ""}
            />
        </label>
    {:else}
        {#each langs as lang}
            <div class="inline">
                <label for="endText" class="text-slate-600"
                    >{traduction.logo_endtext}
                    <span class="text-xs">{lang.lang} </span>
                    <input
                        on:blur={() => (needsUpdate = true)}
                        type="text"
                        name="closing_text_{lang.lang}"
                        class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                        value={lang.closingText}
                    />
                </label>
            </div>
        {/each}
    {/if}

    <label for="color" class="text-slate-600 pt-1">
        {traduction.logo_color}
        <input
            on:blur={() => (needsUpdate = true)}
            type="color"
            name="color"
            bind:value={color}
            class="my-4 rounded py-1"
        />
    </label>
    <div class="w-full mx-auto text-center py-5">
        <button
            type="submit"
            class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
            {disabled}
        >
            <p class="text-center mx-auto">
                {@html submitText}
            </p>
        </button>
    </div>
</form>
<p class="text-sm text-slate-500 ml-8">
    *{traduction.logo_html}
</p>
