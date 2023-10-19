<script lang="ts">
    export let FBLink = "";
    export let InstaLink = "";
    export let TwitterLink = "";
</script>

<div class="scocials text-white w-full flex items-center justify-center">
    <!-- Insta -->
    {#if InstaLink}
        <a href={InstaLink} class="mt-0.5 mx-5">
            <svg width="1.12em" height="1.12em" viewBox="0 0 20 20"
                ><path
                    fill="currentColor"
                    d="M17 1H3c-1.1 0-2 .9-2 2v14c0 1.101.9 2 2 2h14c1.1 0 2-.899 2-2V3c0-1.1-.9-2-2-2zM9.984 15.523a5.539 5.539 0 0 0 5.538-5.539c0-.338-.043-.664-.103-.984H17v7.216a.69.69 0 0 1-.693.69H3.693a.69.69 0 0 1-.693-.69V9h1.549c-.061.32-.104.646-.104.984a5.54 5.54 0 0 0 5.539 5.539zM6.523 9.984a3.461 3.461 0 1 1 6.922 0a3.461 3.461 0 0 1-6.922 0zM16.307 6h-1.615A.694.694 0 0 1 14 5.308V3.691c0-.382.31-.691.691-.691h1.615c.384 0 .694.309.694.691v1.616c0 .381-.31.693-.693.693z"
                /></svg
            >
        </a>
    {/if}
    <!-- Facebok -->
    {#if FBLink}
        <a href={FBLink} class="mx-5">
            <svg width="1.2em" height="1.2em" viewBox="0 0 24 24"
                ><path
                    fill="currentColor"
                    d="M20.9 2H3.1A1.1 1.1 0 0 0 2 3.1v17.8A1.1 1.1 0 0 0 3.1 22h9.58v-7.75h-2.6v-3h2.6V9a3.64 3.64 0 0 1 3.88-4a20.26 20.26 0 0 1 2.33.12v2.7H17.3c-1.26 0-1.5.6-1.5 1.47v1.93h3l-.39 3H15.8V22h5.1a1.1 1.1 0 0 0 1.1-1.1V3.1A1.1 1.1 0 0 0 20.9 2Z"
                /></svg
            >
        </a>
    {/if}
    <!-- twitter -->
    {#if TwitterLink}
        <a href={TwitterLink} class="mx-5">
            <svg width="1em" height="1em" viewBox="0 0 1536 1536"
                ><path
                    fill="currentColor"
                    d="M1280 482q-56 25-121 34q68-40 93-117q-65 38-134 51q-61-66-153-66q-87 0-148.5 61.5T755 594q0 29 5 48q-129-7-242-65T326 422q-29 50-29 106q0 114 91 175q-47-1-100-26v2q0 75 50 133.5T461 885q-29 8-51 8q-13 0-39-4q21 63 74.5 104t121.5 42q-116 90-261 90q-26 0-50-3q148 94 322 94q112 0 210-35.5t168-95t120.5-137t75-162T1176 618q0-18-1-27q63-45 105-109zm256-194v960q0 119-84.5 203.5T1248 1536H288q-119 0-203.5-84.5T0 1248V288Q0 169 84.5 84.5T288 0h960q119 0 203.5 84.5T1536 288z"
                /></svg
            >
        </a>
    {/if}
</div>
