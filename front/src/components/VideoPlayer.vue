<template>
  <div class="video-player">
    <div v-if="videoUrl" class="video-container m-1">
      <iframe
        :src="videoUrl"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
    <div v-else class="video-container m-1">
      <p>No Video Selected</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    videoUrl: String
  }
}
</script>

<style>
.video-player {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-container {
  width: 100vw;
  height: 70vw;
  max-width: 1000px;
  max-height: 562px;
}

.video-container iframe {
  width: 100%;
  height: 100%;
}
</style>
