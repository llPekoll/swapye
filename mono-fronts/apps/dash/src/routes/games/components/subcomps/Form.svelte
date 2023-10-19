<script lang="ts">
    import { enhance } from "$app/forms";
    import { emblem, forms } from "$lib/stores/index";
    import { page } from "$app/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";
    import DropZone from "$lib/components/DropZone.svelte";

    const traduction = $page.data.user.traduction;

    let IntroFormPortrait = $forms.formPortrait;
    let IntroFormLandscape = $forms.formLandscape;

    let clearedPortrait = false;
    const clearPortrait = `/perso/clear/${$emblem}/fromportrait`;
    let clearedLand = false;
    const clearLand = `/perso/clear/${$emblem}/fromlandscape`;
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
    action="?/forms"
    use:enhance={() => {
        submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        return async ({ result }) => {
            if (result.type === "success") {
                $forms.formLandscape = result.data?.formLandscape;
                $forms.formPortrait = result.data?.formPortrait;

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
    <p class="text-center text-3xl font-bold text-slate-800">
        {traduction.img_potrait}
    </p>
    <DropZone
        fileType="image"
        name="IntroFormPortrait"
        src={IntroFormPortrait}
        clearUrl={clearPortrait}
        bind:cleared={clearedPortrait}
        whatItisToUpload="form d'intro portrait"
        bind:needsUpdate
    />
    <div class="pt-10 pb-16">
        <p class="text-center text-3xl font-bold text-slate-800">
            {traduction.img_landscape}
        </p>
        <DropZone
            fileType="image"
            name="IntroFormLandscape"
            src={IntroFormLandscape}
            clearUrl={clearLand}
            bind:cleared={clearedLand}
            whatItisToUpload="form d'intro paysage"
            bind:needsUpdate
        />
    </div>
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
