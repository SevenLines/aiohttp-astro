<template>
  <g>
    <path class="zodiac" :class="name.toLowerCase()" :d="path" />
    <text :font-size="circleWidth / 1.5" dy="circleWidth"
          text-anchor="middle"
          dominant-baseline="middle"
          :x="centerP.x * width / 2"
          :y="centerP.y * width / 2">{{icon}}</text>
  </g>
</template>


<script>
  export default {
    name: 'zodiac',
    props: ['start', 'end', 'name', 'width', 'icon', 'circle-width'],
    computed: {
      centerP () {
        return {
          y: Math.sin((this.start + this.end) / 360 * Math.PI),
          x: Math.cos((this.start + this.end) / 360 * Math.PI)
        }
      },
      startP () {
        return {
          y: Math.sin(this.start / 180 * Math.PI),
          x: Math.cos(this.start / 180 * Math.PI)
        }
      },
      endP () {
        return {
          y: Math.sin(this.end / 180 * Math.PI),
          x: Math.cos(this.end / 180 * Math.PI)
        }
      },
      big () {
        return this.width / 2 + this.circleWidth
      },
      small () {
        return this.width / 2 - this.circleWidth
      },
      path () {
        return `M${this.startP.x * this.big} ${this.startP.y * this.big} ` +
          `A${this.big} ${this.big} 0 0 1 ${this.endP.x * this.big} ${this.endP.y * this.big} ` +
          `L${this.endP.x * this.small} ${this.endP.y * this.small} ` +
          `A${this.small} ${this.small} 0 0 0 ${this.startP.x * this.small} ${this.startP.y * this.small}`
      }
    }
  }
</script>


<style lang="scss" scoped>
  @mixin zodiac($name, $color) {
    .#{$name} {
      fill: rgba($color, 0.05);
      &:hover {
        fill: rgba($color, 0.1);
      }
    }
  }

  .zodiac {
    cursor: pointer;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    -ms-transition: all 0.3s;
    -o-transition: all 0.3s;
    transition: all 0.3s;
    fill: white;
    stroke-width: 1px;
    stroke: black;
    &:hover {
      fill: #e4e4e4;
    }
  }

  @include zodiac('aries', #ff0f32)
  @include zodiac('taurus', #76eb20)
  @include zodiac('gemini', #ffaa00)
  @include zodiac('cancer', #4dffd5)
  @include zodiac('leo', #ffe900)
  @include zodiac('virgo', #00d2ff)
  @include zodiac('libra', #ff0092)
  @include zodiac('scorpio', #c3001a)
  @include zodiac('sagittarius', #ff0087)
  @include zodiac('capricorn', #004bff)
  @include zodiac('aquarius', #ff00f3)
  @include zodiac('pisces', #388dff)

</style>
