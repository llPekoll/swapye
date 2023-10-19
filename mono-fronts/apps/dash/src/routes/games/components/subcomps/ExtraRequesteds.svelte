<script lang="ts">
    import { enhance } from "$app/forms";
    import NewReqElt from "./newReqElt.svelte";

    import AddAccountCard from "$lib/components/AddAccountCard.svelte";
    import { emblem, extraReqReturn } from "$lib/stores/index";
    import { page } from "$app/stores";
    import type { ExtraRequested } from "$lib/types";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";

    const traduction = $page.data.user.traduction;

    const extraLangs = $extraReqReturn.langs;
    let extraElts = $extraReqReturn.extraElements;
    let JJextraElts: ExtraRequested[] = [];

    // const requestedElts: [] = [];
    const addElts = () => {
        console.log("addElts", JJextraElts.length);
        let newNeqElt: ExtraRequested = {
            key: "",
            wordings: [],
            kind: "",
        };
        JJextraElts = [...JJextraElts, newNeqElt];
    };

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
    action="?/extrarequesteds"
    use:enhance={({ form }) => {
        submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        return async ({ result, update }) => {
            if (result.type === "success") {
                $extraReqReturn.langs = result.data?.langs;
                $extraReqReturn.extraElements = result.data?.extraElements;
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
    {@html traduction.extraRequesteds_explanation_rich}
    <input type="hidden" name="emblem" value={$emblem} />

    {#if extraElts}
        {#each extraElts as elt, i}
            <NewReqElt {extraLangs} {elt} {i} bind:needsUpdate />
        {/each}
    {/if}

    {#each JJextraElts as JJextraElt, i}
        <NewReqElt
            {extraLangs}
            {JJextraElt}
            i={extraElts.length + i}
            bind:needsUpdate
        />
    {/each}
    <div on:click={addElts} on:keydown={addElts}>
        <AddAccountCard />
    </div>
    <div class="w-full flex items-center justify-center py-5">
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
