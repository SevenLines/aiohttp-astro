<template>
  <div class="zodiac">
    <div class="left border" :style="leftBorderStyle"></div>
    <div class="icon" :style="iconStyle">{{icon}}</div>
    <div class="right border" :style="rightBorderStyle"></div>
  </div>
</template>


<script>
  export default {
    name: 'zodiac',
    props: ['start', 'end', 'name', 'width', 'icon', 'circle-width'],
    computed: {
      length () {
        return this.width / 2
      },
      iconStyle () {
        let angle = (this.start + this.end) / 2
        return {
          transform: `translate(-50%, -50%) rotate(${angle}deg) translate(${this.length}px, 0)  rotate(90deg)`
        }
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
    .border, .icon {


      left: 50%;
      top: 50%;
      position: absolute;
    }
    .icon {
      font-size: 1.5em;
      font-weight: bold;

    }
    .border {
      -webkit-transition: all 0.1s;
      -moz-transition: all 0.1s;
      -ms-transition: all 0.1s;
      -o-transition: all 0.1s;
      transition: all 0.1s;
      width: 1px;
      background-color: black;
    }
    &:hover {
      .icon {
        text-shadow: 0 0 6px silver;
      }
    }
  }
</style>
