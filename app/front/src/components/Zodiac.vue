<template>
  <div class="zodiac">
    <div class="left border" :style="leftBorderStyle"></div>
    <div class="right border" :style="rightBorderStyle"></div>
  </div>
</template>


<script>
  export default {
    name: 'zodiac',
    props: ['start', 'end', 'name', 'width', 'circle-width'],
    computed: {
      length () {
        return this.width / 2
      },
      leftBorderStyle () {
        return {
          transform: `translate(-50%, -50%) rotate(${this.start}deg) translate(${this.length}px, 0) rotate(90deg)`,
          height: `${this.circleWidth * 2}px`
        }
      },
      rightBorderStyle () {
        return {
          transform: `translate(-50%, -50%) rotate(${this.end}deg) translate(${this.length}px, 0) rotate(90deg)`,
          height: `${this.circleWidth * 2}px`
        }
      }
    }
  }
</script>


<style lang="scss" scoped>
  .zodiac {
    .border {
      left: 50%;
      top: 50%;
      position: absolute;
      width: 1px;
      background-color: black;
    }
  }
</style>
