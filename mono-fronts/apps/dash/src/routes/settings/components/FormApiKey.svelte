<script lang="ts">
    import { enhance } from "$app/forms";
    import Input from "$lib/components/Input.svelte";
    import { page } from "$app/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";
    import { apiKey } from "$lib/stores";

    // Variables
    const traduction = $page.data.user.traduction;

    let providers = $apiKey.providers;
    let provider = $apiKey.provider || providers[0];
    let apikey = $apiKey.apikey;
    let apisecret = $apiKey.apipass;
    let email = $apiKey.email;
    let EmailName = $apiKey.display_name;

    // Form
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

<div class="my-2 py-2 px-5 mx-10">
    <form
        class="py-6"
        method="POST"
        action="?/apikey"
        use:enhance={({ form }) => {
            submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
            submitColor = "bleu-gris/[.3]";
            cursor = "cursor-not-allowed";
            return async ({ result, update }) => {
                if (result.type === "success") {
                    $apiKey.apikey = result.data?.apikey;
                    $apiKey.apipass = result.data?.apipass;
                    $apiKey.provider = result.data?.provider;
                    $apiKey.email = result.data?.email;
                    $apiKey.display_name = result.data?.display_name;
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
        <div
            on:click={() => (needsUpdate = true)}
            on:keypress={() => (needsUpdate = true)}
        >
            <label for="margin" class=" text-gray-500 font-bold mb-1 pr-4">
                {traduction.email_provider_apikey}
            </label>
            <select
                name="provider"
                bind:value={provider}
                class=" py-1.5 rounded-md border border-gray-300 pl-3"
            >
                {#each providers as prv}
                    <option value={prv}>{prv}</option>
                {/each}
            </select>
        </div>

        <Input
            name={traduction.apisecret_apikey}
            bind:val={apisecret}
            inputName="secret"
            bind:needsUpdate
        />
        <Input
            name={traduction.apikey_apikey}
            bind:val={apikey}
            inputName="key"
            bind:needsUpdate
        />
        <Input
            name={traduction.email_use_apikey}
            bind:val={email}
            inputName="email"
            bind:needsUpdate
        />
        <Input
            name={traduction.name_use_apikey}
            bind:val={EmailName}
            inputName="displayName"
            bind:needsUpdate
        />

        <button
            type="submit"
            class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
            data-test="submit"
            {disabled}
        >
            <p class="text-center mx-auto">
                {@html submitText}
            </p>
        </button>
    </form>
</div>
