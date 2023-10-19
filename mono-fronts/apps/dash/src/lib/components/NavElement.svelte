<script>
    export let icon = "";
    export let title = "";
    export let link = "";
    export let gameEdition = false;
    import { page } from "$app/stores";

    let blue = "";
    if ($page.url.pathname.includes(link)) {
        blue = "swapye-primary";
    } else {
        blue = "swapye-gray-bright";
    }
    const dataTest = `${title}-menu`;
</script>

<li class="md:col-start-1 md:col-end-4 px-2 md:block md:py-3">
    <a
        data-test={dataTest}
        data-sveltekit-preload-data="hover"
        href={link}
        class="mx-auto text-center md:flex-none flex"
    >
        <span class="mt-1.5 svgvg {blue} mt-4 md:mt-1">{@html icon}</span>
        {#if !gameEdition}
            <span class="md:pl-3 md:inline ml-3 {blue} hidden font-light"
                >{title}</span
            >
        {/if}
        <!-- <span class="md:pl-3 md:inline ml-3 {blue} hidden font-light"
            >{title}</span
        > -->
        <!-- <div class="ml-9 md:ml-14 absolute mt-7" class:active={$page.url.pathname.includes(link)} /> -->
    </a>
</li>

<style>
    .active {
        background-color: #8fcfb1;
        width: 5px;
        height: 5px;
        border-radius: 50px;
    }
    .svgvg {
        transform: scale(2);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }
</style>
