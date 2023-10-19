<script lang="ts">
    import { enhance } from "$app/forms";
    import { emblem } from "$lib/stores/index";
    import { page } from "$app/stores";

    const traduction = $page.data.user.traduction;
    let facebook: string;
    let insta: string;
    let twitter: string;
    const yo = async () => {
        const url = `/perso/${$emblem}/socials`;
        const res = await fetch(url);
        const data = await res.json();
        facebook = data.facebook;
        insta = data.insta;
        twitter = data.twitter;
    };
    yo();
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";
</script>

<form
    class="w-full px-10 pt-10"
    enctype="multipart/form-data"
    method="POST"
    action="?/socials"
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

    <div>
        <!-- Facebook -->
        <div class="py-1.5">
            <label for="facebook" class="flex text-slate-600 ">
                <svg width="2.2em" height="2.2em" viewBox="0 0 24 24"
                    ><path
                        fill="currentColor"
                        d="M20.9 2H3.1A1.1 1.1 0 0 0 2 3.1v17.8A1.1 1.1 0 0 0 3.1 22h9.58v-7.75h-2.6v-3h2.6V9a3.64 3.64 0 0 1 3.88-4a20.26 20.26 0 0 1 2.33.12v2.7H17.3c-1.26 0-1.5.6-1.5 1.47v1.93h3l-.39 3H15.8V22h5.1a1.1 1.1 0 0 0 1.1-1.1V3.1A1.1 1.1 0 0 0 20.9 2Z"
                    /></svg
                >
                <input
                    type="url"
                    name="facebook"
                    class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500 ml-2"
                    value={facebook}
                />
            </label>
        </div>
        <!-- insta -->
        <div class="">
            <label for="insta" class="flex text-slate-600">
                <svg width="2em" height="2em" viewBox="0 0 20 20"
                    ><path
                        fill="currentColor"
                        d="M17 1H3c-1.1 0-2 .9-2 2v14c0 1.101.9 2 2 2h14c1.1 0 2-.899 2-2V3c0-1.1-.9-2-2-2zM9.984 15.523a5.539 5.539 0 0 0 5.538-5.539c0-.338-.043-.664-.103-.984H17v7.216a.69.69 0 0 1-.693.69H3.693a.69.69 0 0 1-.693-.69V9h1.549c-.061.32-.104.646-.104.984a5.54 5.54 0 0 0 5.539 5.539zM6.523 9.984a3.461 3.461 0 1 1 6.922 0a3.461 3.461 0 0 1-6.922 0zM16.307 6h-1.615A.694.694 0 0 1 14 5.308V3.691c0-.382.31-.691.691-.691h1.615c.384 0 .694.309.694.691v1.616c0 .381-.31.693-.693.693z"
                    /></svg
                >
                <input
                    type="url"
                    name="insta"
                    class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500 ml-2"
                    value={insta}
                />
            </label>
        </div>
        <!-- twitter -->
        <div class="py-1.5">
            <label for="twitter" class="flex text-slate-600">
                <svg width="2em" height="2em" viewBox="0 0 1536 1536"
                    ><path
                        fill="currentColor"
                        d="M1280 482q-56 25-121 34q68-40 93-117q-65 38-134 51q-61-66-153-66q-87 0-148.5 61.5T755 594q0 29 5 48q-129-7-242-65T326 422q-29 50-29 106q0 114 91 175q-47-1-100-26v2q0 75 50 133.5T461 885q-29 8-51 8q-13 0-39-4q21 63 74.5 104t121.5 42q-116 90-261 90q-26 0-50-3q148 94 322 94q112 0 210-35.5t168-95t120.5-137t75-162T1176 618q0-18-1-27q63-45 105-109zm256-194v960q0 119-84.5 203.5T1248 1536H288q-119 0-203.5-84.5T0 1248V288Q0 169 84.5 84.5T288 0h960q119 0 203.5 84.5T1536 288z"
                    /></svg
                >
                <input
                    type="url"
                    name="twitter"
                    class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500 ml-2"
                    value={twitter}
                />
            </label>
        </div>
    </div>
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
