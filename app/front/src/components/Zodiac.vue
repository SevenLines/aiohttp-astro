<template>
  <g class="zodiac" :class="name.toLowerCase()">
    <path :d="path"/>
    <text :font-size="circleWidth / 1.5"
          :x="centerP.x * width / 2"
          :y="centerP.y * width / 2">{{icon}}
    </text>
    <path class="sub" :class="name.toLowerCase()" :d="generatePie(small, small-10, start, end)"/>
  </g>
</template>


<script>
  export default {
    name: 'zodiac',
    props: ['start', 'end', 'name', 'width', 'icon', 'circle-width'],
    methods: {
      generatePie (big, small, startAngle, endAngle) {
        let startP = {
          y: Math.sin(Math.radians(-startAngle)),
          x: Math.cos(Math.radians(-startAngle))
        }
        let endP = {
          y: Math.sin(Math.radians(-endAngle)),
          x: Math.cos(Math.radians(-endAngle))
        }
        return `M${startP.x * big} ${startP.y * big} ` +
          `A${big} ${big} 0 0 0 ${endP.x * big} ${endP.y * big} ` +
          `L${endP.x * small} ${endP.y * small} ` +
          `A${small} ${small} 0 0 1 ${startP.x * small} ${startP.y * small}`
      }
    },
    computed: {
      centerP () {
        return {
          y: Math.sin(-(this.start + this.end) / 360 * Math.PI),
          x: Math.cos(-(this.start + this.end) / 360 * Math.PI)
        }
      },
      big () {
        return this.width / 2 + this.circleWidth
      },
      small () {
        return this.width / 2 - this.circleWidth
      },
      path () {
        return this.generatePie(this.big, this.small, this.start, this.end)
      }
    }
  }
</script>


<style lang="scss" scoped>
  @mixin zodiac($name, $color) {
    .#{$name} {
      path {
        fill: rgba($color, 0.25);
      }
      path.sub {
        fill: rgba($color, 0.35);
      }
      &:hover {
        path {
          &.sub {
            fill: rgba($color, 0.65);
          }
          fill: rgba($color, 0.35);
        }
      }
    }
  }

  .zodiac {
    text {
      color: black;
      text-anchor: middle;
      dominant-baseline: middle;
    }
    path {
      cursor: pointer;
      -webkit-transition: all 0.3s;
      -moz-transition: all 0.3s;
      -ms-transition: all 0.3s;
      -o-transition: all 0.3s;
      transition: all 0.3s;
      fill: white;
      stroke-width: 4px;
      stroke: #ffffff;
    }

  }

  @include zodiac('aries', #ff0f32)
  @include zodiac('taurus', #eb5c00)
  @include zodiac('gemini', #ffaa00)
  @include zodiac('cancer', #ffed00)
  @include zodiac('leo', #caff00)
  @include zodiac('virgo', #29ff00)
  @include zodiac('libra', #00ffa1)
  @include zodiac('scorpio', #0098c3)
  @include zodiac('sagittarius', #0068ff)
  @include zodiac('capricorn', #6e00ff)
  @include zodiac('aquarius', #cb00ff)
  @include zodiac('pisces', #ff00de)

</style>
