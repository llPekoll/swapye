<script lang="ts">
    export let src: string = "";
    export let lang: string = "";
    export let updaloed = false;

    let img: HTMLElement;
    let showImage = false;
    if (src) {
        updaloed = true;
    }
    const onChange = (e: Event) => {
        const elt = e.target as HTMLFormElement;
        const file = elt.files[0];
        if (file) {
            showImage = true;

            const reader = new FileReader();
            reader.addEventListener("load", function () {
                img.setAttribute("src", reader.result as string);
            });
            reader.readAsDataURL(file);
            return;
        }
        showImage = false;
    };
</script>

<div>
    {#if updaloed && !showImage}
        {#if src}
            <img
                {src}
                alt="Preview"
                class=" max-w-32 max-h-32 text-center mx-auto rounded-lg"
            />
        {:else}
            <div class="w-full">
                <p class="text-9xl not-italic flex justify-center">🎁</p>
            </div>
        {/if}
    {/if}
    {#if showImage}
        <img
            bind:this={img}
            src=""
            alt="Preview"
            class="max-w-32 max-h-32 text-center mx-auto rounded-lg"
        />
    {/if}
    <label for="img-{lang}" class="flex">
        image
        <span class="text-xs pt-2">
            {lang}
        </span></label
    >
    <input
        on:change={onChange}
        name="img-{lang}"
        type="file"
        accept="image/png, image/jpg, image/jpeg, image/gif"
    />
</div>
