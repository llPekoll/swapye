<script>
    import { onMount } from "svelte";

    export let submitModale;
    export let src = "";
    export let is_winner;
    export let dayNb;
    export let skin = 1;
    const mode = () => {
        if (is_winner) {
            submitModale = true;
        }
    };
    let loaded = false;
    let failed = false;
    let loading = false;

    onMount(() => {
        const img = new Image();
        img.src = src;
        loading = true;
        img.onload = () => {
            loading = false;
            loaded = true;
        };
        img.onerror = () => {
            loading = false;
            failed = true;
        };
    });
</script>

{#if loaded}
    <div
        class="md:mx-10 md:my-6 mx-4 {skin == 2
            ? 'w-24 h-28'
            : 'w-20 h-24'} bg-fill my-2 text-center cursor-pointer"
        on:click={mode}
        on:keyup={mode}
    >
        <div class="md:scale-150 scale-100">
            <img
                class="hover:scale-110 hover:duration-200 "
                {src}
                alt="door-{dayNb}"
            />
        </div>
    </div>
{/if}
