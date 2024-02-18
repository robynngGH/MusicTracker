console.log('Star Rating Widget JavaScript loaded');
odoo.define('musictracker.star_rating_widget', function (require) {
    'use strict';

    const { Component, useState, useExternalListener } = owl;
    const { useRef } = owl.hooks;
    const { registerField } = require('web.field_registry');

    class StarRatingWidget extends Component {
        constructor() {
            super(...arguments);
            this.maxValue = 5;
            this.value = 0;
        }

        setup() {
            useExternalListener(window, 'mouseup', this._onMouseUp.bind(this));
            this.inputRef = useRef('starRatingInput');
            registerField('star_rating', this.inputRef);
        }

        _onStarClick(ev) {
            const index = ev.target.dataset.index;
            this.value = index + 1;
        }

        _onMouseUp() {
            this.trigger('field_changed', {
                dataPointID: this.cpID,
                changes: { rating: this.value },
            });
        }

        renderStar(index) {
            return (
                <i
                    key={index}
                    class={`o_star_rating_widget_star fa ${
                        index < this.value ? 'fa-star' : ''
                    } ${index === this.value && this.value % 1 !== 0 ? 'fa-star-half-alt' : 'far fa-star'}`}
                    data-index={index}
                    onClick={this._onStarClick.bind(this)}
                ></i>
            );
        }

        render() {
            return (
                <div class="o_star_rating_widget">
                    {Array.from({ length: this.maxValue }, (_, index) => this.renderStar(index))}
                </div>
            );
        }
    }

    return StarRatingWidget;
});