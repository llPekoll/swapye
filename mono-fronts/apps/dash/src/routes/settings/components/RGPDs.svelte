<!-- <script lang="ts">
    import { slide } from "svelte/transition";
    import { enhance } from "$app/forms";
    // @ts-ignore
    import { quill } from "svelte-quill";
    import { page } from "$app/stores";
    const traduction = $page.data.user.traduction;
    const options = {
        modules: {
            toolbar: [
                [{ header: [1, 2, 3, false] }],
                ["bold", "italic", "underline", "strike"],
                ["link", "code-block", "blockquote"],
                [{ script: "sub" }, { script: "super" }],
                [{ list: "ordered" }, { list: "bullet" }],
                [{ indent: "-1" }, { indent: "+1" }],
                [{ font: [] }],
                [{ align: [] }],
                [{ color: [] }, { background: [] }],
                ["clean"],
            ],
        },
        placeholder: "Type something...",
        theme: "bubble",
    };

    export let regulation: string = "";
    // export let policyRules: string = "";
    let isOpen = false;
    const toggle = () => (isOpen = !isOpen);
    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";

    let contentRegulation = "";
    let contentPolicyRules = "";
</script>

<svelte:head>
    <link href="//cdn.quilljs.com/1.3.6/quill.bubble.css" rel="stylesheet" />
</svelte:head>

<div class=" text-slate-700">
    <button on:click={toggle} aria-expanded={isOpen} class="text-4xl z-10">
        <svg
            class="inline"
            style="tran"
            width="20"
            height="20"
            fill="none"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
            <path d="M9 5l7 7-7 7" />
        </svg>
        RGPDs
    </button>
</div>
{#if isOpen}
    <div
        transition:slide={{ duration: 300 }}
        class="my-2 py-2 bg-slate-100 px-5 rounded-lg mx-10"
    >
        <form
            class="py-6"
            method="POST"
            action="?/rgpds"
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
            {#if contentRegulation}
                <input
                    type="hidden"
                    name="regulation"
                    value={contentRegulation.html}
                />
            {/if}
            {#if contentPolicyRules}
                <input
                    type="hidden"
                    name="regulation"
                    value={contentPolicyRules.html}
                />
            {/if}
            Policy
            <div
                class="editor bg-white rounded-lg"
                use:quill={options}
                on:text-change={(e) => (contentPolicyRules = e.detail)}
            />
            Regulation
            <div
                class="editor"
                use:quill={options}
                on:text-change={(e) => (regulation = e.detail)}
            />

            <button
                type="submit"
                class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
            >
                <p class="text-center mx-auto">
                    {@html submitText}
                </p>
            </button>
        </form>
    </div>
{/if}

<style>
    button {
        cursor: pointer;
    }

    svg {
        transition: transform 0.2s ease-in;
    }

    [aria-expanded="true"] svg {
        transform: rotate(0.25turn);
    }
</style> -->
