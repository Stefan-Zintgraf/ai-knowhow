<template>
  <Progress 
    level="2"
    position="top"
    :opacity="0.3"
    activeColor="#3b82f6"
    barColor="#e5e7eb"
    thickness="4px"
    transitionDuration="200ms"
  />
</template>

<style scoped>
:deep(.progress-bar) {
  backdrop-filter: blur(4px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

:deep(.progress-bar:hover) {
  opacity: 0.9 !important;
}
</style>