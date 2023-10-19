<script lang="ts">
    import { enhance } from "$app/forms";
    import CheckBox from "$lib/components/CheckBox.svelte";

    import { emblem } from "$lib/stores/index";
    import { page } from "$app/stores";
    const traduction = $page.data.user.traduction;

    let override_email_check = false;
    let permission_list: string[] = ["some_permission"];

    const yo = async () => {
        const url = `/perso/${$emblem}/payableOptions`;
        const res = await fetch(url);
        const data = await res.json();
        console.log({ data });
        override_email_check = data.email_check;
        permission_list = data.can_access_to;
        if (permission_list === undefined) permission_list = [];
    };
    yo();
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";
</script>

<form
    class="w-full px-10 pt-10"
    method="POST"
    action="?/payableOptions"
    use:enhance={({ form }) => {
        submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        return async ({ result, update }) => {
            submitText = traduction.submit;
            submitColor = "bleu-gris";
            cursor = "cursor-pointer";
        };
    }}
>
    <input type="hidden" name="emblem" value={$emblem} />
    {#if permission_list.includes("email_validator")}
        <CheckBox
            tradsToDisp={traduction.override_email_check}
            bind:valueToSet={override_email_check}
            name="email_check"
        />
    {:else}
        Vous n'avez pas les droits pour modifier cette option
    {/if}

    <div class="w-full flex items-center justify-center py-5">
        <button
            type="submit"
            class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
        >
            <p class="text-center mx-auto">
                {@html submitText}
            </p>
        </button>
    </div>
</form>
