<script lang="ts">
    export let fileType: string = "image" || "sound";
    export let whatItisToUpload: string = "Logo" || "Sound" || "Image";
    export let name: string = "";
    export let src: string | null = "";
    export let clearUrl: string = "";
    export let cleared: boolean = false;
    export let needsUpdate: boolean = false;

    let img: HTMLElement | null;
    let source: HTMLElement;
    let showElt = false;
    let fileKind = fileType;
    let acceptedFileTypes = "";
    const imgType = "image/png, image/jpg, image/jpeg, image/gif";

    if (fileType === "image") {
        fileType = imgType;
        acceptedFileTypes = "PNG, JPG, JPEG, GIF";
    } else if (fileType === "sound") {
        fileType = ".mp3,audio/*";
        acceptedFileTypes = "MP3, WAV";
    }

    function makeid(length: number) {
        let result = "";
        const characters =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        const charactersLength = characters.length;
        let counter = 0;
        while (counter < length) {
            result += characters.charAt(
                Math.floor(Math.random() * charactersLength)
            );
            counter += 1;
        }
        return result;
    }
    if (src) {
        src = `${src}?${makeid(5)}`;
    }
    const onChange = (e: Event): void => {
        const elt = e.target as HTMLFormElement;
        const file = elt.files[0];
        if (file) {
            showElt = true;
            const reader = new FileReader();
            if (img === undefined) {
                img = document.createElement("img");
            }
            if (source === undefined) {
                source = document.createElement("audio");
            }
            reader.addEventListener("load", function () {
                if (fileType === imgType) {
                    img?.setAttribute("src", reader.result as string);
                } else {
                    source.setAttribute("src", reader.result as string);
                }
            });
            reader.readAsDataURL(file);

            return;
        }
        showElt = false;
    };

    const clear = async () => {
        if (!confirm("supprimer cet element ?")) {
            return;
        }

        await fetch(clearUrl, {
            method: "DELETE",
        });
        cleared = true;
    };
</script>

{#if !cleared}
    {#if fileKind === "image" || fileKind === imgType}
        {#if !showElt && src}
            <div class="flex justify-center">
                <img
                    {src}
                    alt="Preview with src"
                    class="h-32 py-3 rounded-lg inline"
                />
                <div on:click={clear} on:keyup={clear} class="py-4 inline">
                    <svg
                        class="fill-red-500"
                        width="2em"
                        height="2em"
                        viewBox="0 0 24 24"
                    >
                        <path
                            d="M12 3c-4.963 0-9 4.038-9 9s4.037 9 9 9s9-4.038 9-9s-4.037-9-9-9zm0 16c-3.859 0-7-3.14-7-7s3.141-7 7-7s7 3.14 7 7s-3.141 7-7 7zm.707-7l2.646-2.646a.502.502 0 0 0 0-.707a.502.502 0 0 0-.707 0L12 11.293L9.354 8.646a.5.5 0 0 0-.707.707L11.293 12l-2.646 2.646a.5.5 0 0 0 .707.708L12 12.707l2.646 2.646a.5.5 0 1 0 .708-.706L12.707 12z"
                        /></svg
                    >
                </div>
            </div>
        {/if}
        {#if showElt && img}
            <img
                bind:this={img}
                src=""
                alt="Preview"
                class="h-32 text-center mx-auto mt-10 py-3 rounded-lg"
            />
        {/if}
    {:else}
        {#if !showElt && src}
            <div class="flex items-center justify-center">
                <audio controls {src} class="py-3">
                    <source {src} class="py-3" />
                </audio>
                <div on:click={clear} on:keyup={clear} class="py-4">
                    <svg
                        class="fill-red-500"
                        width="2em"
                        foi
                        height="2em"
                        viewBox="0 0 24 24"
                    >
                        <path
                            d="M12 3c-4.963 0-9 4.038-9 9s4.037 9 9 9s9-4.038 9-9s-4.037-9-9-9zm0 16c-3.859 0-7-3.14-7-7s3.141-7 7-7s7 3.14 7 7s-3.141 7-7 7zm.707-7l2.646-2.646a.502.502 0 0 0 0-.707a.502.502 0 0 0-.707 0L12 11.293L9.354 8.646a.5.5 0 0 0-.707.707L11.293 12l-2.646 2.646a.5.5 0 0 0 .707.708L12 12.707l2.646 2.646a.5.5 0 1 0 .708-.706L12.707 12z"
                        /></svg
                    >
                </div>
            </div>
        {/if}
        {#if showElt}
            <audio
                bind:this={source}
                src=""
                controls
                class="h-32 text-center mx-auto py-3 rounded-lg"
            />
        {/if}
    {/if}
{/if}
<label
    for="dropzone-file-{name}"
    class="mx-auto text-center flex flex-col justify-center items-center w-1/2 h-20 bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
>
    <div class="flex flex-col justify-center items-center pt-5 pb-6">
        <svg
            aria-hidden="true"
            class="-mb-1 w-10 h-10 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            ><path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            /></svg
        >
        <p class="-mb-1 text-sm text-gray-500 dark:text-gray-400">
            <span class="font-semibold"
                >Click to upload your {whatItisToUpload}</span
            >
        </p>
        <p class="text-xs text-gray-500 dark:text-gray-400">
            {acceptedFileTypes}
        </p>
    </div>
    <input
        on:change={onChange}
        on:blur={() => {
            cleared = false;
            needsUpdate = true;
        }}
        id="dropzone-file-{name}"
        {name}
        type="file"
        accept={fileType}
    />
</label>
