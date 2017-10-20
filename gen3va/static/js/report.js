/**
 * Custom Axis extension to allow emulation of negative values on a logarithmic
 * Y axis. Note that the scale is not mathematically correct, as a true
 * logarithmic axis never reaches or crosses zero.
 */
(function (H) {
    // Pass error messages
    H.Axis.prototype.allowNegativeLog = true;

    // Override conversions
    H.Axis.prototype.log2lin = function (num) {
        var isNegative = num < 0,
            adjustedNum = Math.abs(num),
            result;
        if (adjustedNum < 10) {
            adjustedNum += (10 - adjustedNum) / 10;
        }
        result = Math.log(adjustedNum) / Math.LN10;
        return isNegative ? -result : result;
    };
    H.Axis.prototype.lin2log = function (num) {
        var isNegative = num < 0,
            absNum = Math.abs(num),
            result = Math.pow(10, absNum);
        if (result < 10) {
            result = (10 * (result - 1)) / (10 - 1);
        }
        return isNegative ? -result : result;
    };
}(Highcharts));


function createAndManageVisualizations(config) {

    var clustergrams = {},
        originalData = {};

    $(function() {
        var elem;
        if (config.hasDataTable){
            setupDataTables();    
        }
        resizeClustergramsOnWindowResize();
        try {
            elem = '#dx-plot';
            plotBar(config.barPlotDx, 'dx-plot');
        } catch (e) {
            $(elem).hide();
            console.log(e);
        }
        try {
            elem = '#dx-bubble-plot';
            plotBubble(config.barPlotDx, 'dx-bubble-plot');
        } catch (e) {
            $(elem).hide();
            console.log(e);
        }
        try {
            elem = '#rx-plot';
            plotBar(config.barPlotRx, 'rx-plot');
        } catch (e) {
            $(elem).hide();
            console.log(e);
        }
        try {
            elem = '#rx-bubble-plot';
            plotBubble(config.barPlotRx, 'rx-bubble-plot');
        } catch (e) {
            $(elem).hide();
            console.log(e);
        }

        try {
            elem = '#kde-plot';
            plotKDE(config.kdeObj, 'kde-plot')
        } catch (e) {
            $(elem).hide();
            console.log(e);
        }
    });

    /* Creates the Enrichr clustergrams.
     */
    function createAndWatchEnrichrHeatMaps(elem, enrichrHeatMaps) {
        var $enrichr = $(elem),
            len = length(enrichrHeatMaps),
            heatMap,
            root,
            i;
        for (i = 0; i < len; i++) {
            heatMap = enrichrHeatMaps[i];
            root = '#' + heatMap.enrichr_library;
            $enrichr.append(
                '<div ' +
                '   id="' + heatMap.enrichr_library + '"' +
                '   class="heat-map enrichr-heat-map"' +
                '></div>'
            );
            createClustergram(root, heatMap);
        }

        showEnrichrHeatMap(enrichrHeatMaps[0].enrichr_library);
        changeEnrichrClustergramOnSelectChange($enrichr, enrichrHeatMaps);
    }

    /* Creates a new clustergram, caching the original data so we can "reset"
     * it later.
     */
    function createClustergram(root, data) {

        var hasCategory = typeof data.network.col_nodes[0]['cat-0'] !== 'undefined',
            catIdx = hasCategory ? '1' : '0';

        addDuplicateHlights(catIdx, data.network.col_nodes, data.network.views);

        var clustergram = Clustergrammer({
            root: root,
            // This specifies the filtering for the clustergram.
            // For more, see:
            // https://github.com/MaayanLab/clustergrammer.js/blob/master/load_clustergram.js
            ini_view: {N_row_sum :50},
            network_data: data.network
        });
        originalData[root] = data;
        try {
            if (hasCategory) {
                makeClustergramColorLegend(root, clustergram.params.viz.cat_colors.col['cat-0']);
            }
            fixClustergramControlsStyling(root);
        } catch (e) {
            console.log(e);
        }
        try {
            filterClustergramColsOnClick(clustergram);
        } catch (e) {
            console.log(e);
        }
        clustergrams[root] = clustergram;
    }

    /* Provides highlights for duplicate datasets. For example, if two
     * signatures came from the same GSE, we want the user to know that.
     */
    function addDuplicateHlights(catIdx, colNodes, views) {
        var uniqueNames = {},
            uniqueNamesIndices;

        colNodes.forEach(function(col, i) {
            var cName = cleanName(col.name);
            if (typeof uniqueNames[cName] === 'undefined') {
                uniqueNames[cName] = 1;
            } else {
                uniqueNames[cName]++;
            }
        });

        uniqueNamesIndices = Object.keys(uniqueNames);
        colNodes.forEach(function(col, i) {
            var cName = cleanName(col.name);
            if (uniqueNames[cName] === 1) {
                col['cat-' + catIdx] = 'dataset: ' + cName;
                col['cat_' + catIdx + '_index'] = 0;
            } else {
                col['cat-' + catIdx] = 'dataset: ' + cName;
                col['cat_' + catIdx + '_index'] = uniqueNamesIndices.indexOf(cName) + 1;
            }
        });

        if (views) {
            views.forEach(function(view, i) {
                addDuplicateHlights(catIdx, view.nodes.col_nodes, undefined);
            });
        }
    }

    /* When the user single-clicks on a column, remove it.
     */
    function filterClustergramColsOnClick(clustergram) {
        d3.selectAll(clustergram.config.root + ' .col_label_text').on('click.report', function(d) {
            if (d3.event.shiftKey) {
                var colToHide = d.name;
                hideColumn(clustergram, colToHide);
                hideD3Tooltips();
                makeClustergramResetButton(clustergram);
            }
        });
    }

    /* Hides a clustergram column based on column name.
     */
    function hideColumn(clustergram, colToHide) {
        var allCols = clustergram.config.network_data.col_nodes_names,
            colsToKeep = remove(allCols, colToHide);
        clustergram.filter_viz_using_names({'col': colsToKeep});
    }

    /* Hides all D3 tooltips after a column has been hidden. This cannot just
     * hide the tooltip for the removed column, because the user can quickly
     * hover over another column before the delayed event happens. Just hide
     * all of them.
     */
    function hideD3Tooltips() {
        $('.d3-tip').css({opacity: 0});
    }

    /* Creates a reset button for each clustergram. This is in case the user
     * filters the columns.
     */
    function makeClustergramResetButton(clustergram) {
        var root = clustergram.config.root,
            buttonAlreadyExists = !!$(root).find('.reset-button').length;
        if (buttonAlreadyExists) {
            return;
        }
        var $button = $(
            '<button class="btn btn-info reset-button">' +
            '   Reset heat map' +
            '</button>'
        );
        $(root).find('.color-legend').after($button);
        $button.click(function() {
            resetClustergram(clustergram);
        });
    }

    function resetClustergram(clustergram) {
        var root = clustergram.config.root,
            data = originalData[root];
        $(root).empty();
        // In `createClustergram`, the new clustergram will step on the old
        // one, but just to be explicit...
        clustergrams[root] = undefined;
        createClustergram(root, data);
    }

    /* Creates the clustergrams' color legends and handles events.
     */
    function makeClustergramColorLegend(root, colors) {
        var list = '',
            isHidden = true,
            MAX_CATS_BEFORE_HIDE = 20,
            $legend,
            $ul,
            $h3;
        $.each(colors, function(categoryName, hex) {
            categoryName = $.trim(categoryName.split(':')[1]);
            var rgb = hexToRgb(hex),
                rgba = 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',.6)';
            list += '' +
                '<li style="border-left: 13px solid ' + rgba + '";>' +
                    categoryName +
                '</li>';
        });
        $legend = $(
            '<div class="color-legend">' +
                '<h3 class="btn btn-info">Show color legend</h3>' +
                '<ul class="list-inline">' +
                    list +
                '</ul>' +
                '<div class="clear"></div>' +
            '</div>'
        );
        $ul = $legend.find('ul');
        $h3 = $legend.find('h3');
        $(root).prepend($legend);
        if (length(colors) > MAX_CATS_BEFORE_HIDE) {
            $ul.hide();
            $h3.click(function(evt) {
                if (isHidden) {
                    isHidden = false;
                    $ul.show();
                    $h3.text('Hide color legend');
                } else {
                    isHidden = true;
                    $ul.hide();
                    $h3.text('Show color legend');
                }
            });
        } else {
            $h3.hide();
        }
    }

    /* Makes modifications to Clustergrammer's default styling:
     * - Removes 15px of left padding so that the controls line up with the
     *   left-hand side of the page
     * - Restyles the sliders so they do not fall off the page.
     */
    function fixClustergramControlsStyling(root) {
        $(root).find(
            '.title_section, .about_section,.icons_section,' +
            '.reorder_section, .gene_search_container,' +
            '.opacity_slider_container, .dendro_sliders, .div_filters'
        ).css({
            'padding-left': '0'
        });
        $('.d3-slider-handle').css({
            'margin-left': '0',
            'width': '.5em'
        });
    }

    /* Changes the Enrichr clustergram based on user selection.
     */
    function changeEnrichrClustergramOnSelectChange($enrichr, enrichrHeatMaps) {
        // When the user selects a new library, toggle the visible library.
        $enrichr.find('select').change(function(evt) {
            var newEnrichrLibrary = $(evt.target).val();
            showEnrichrHeatMap(newEnrichrLibrary);
        });
    }

    /* Shows an Enrichr heat map backed by the provided library.
     */
    function showEnrichrHeatMap(enrichrLibrary) {
        $('.enrichr-heat-map').hide();
        $('#' + enrichrLibrary).show();
    }

    /* Sets up DataTables instances.
     */
    function setupDataTables() {
        $('table').DataTable({ 
            iDisplayLength: 5,
            aLengthMenu: [5, 10, 25, 50, 100],  
        });
    }

    /* Resizes every clustergram when the window is resized. Debounces to
     * prevent overloading the event.
     */
    function resizeClustergramsOnWindowResize() {
        // Debounce this resizing callback because it's fairly intensive.
        $(window).resize(_.debounce(function() {
            $.each(clustergrams, function(i, clustergram) {
                clustergram.resize_viz();
            });
        }, 250));
    }

    /* Removes an item from an array. Credit:
     * http://stackoverflow.com/a/3954451
     */
    function remove(array, item) {
        var index = array.indexOf(item);
        array.splice(index, 1);
        return array
    }

    /* Returns the length of an object.
     */
    function length(obj) {
        var size = 0,
            key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) {
                size++;
            }
        }
        return size;
    }

    /* Converts a hexadecimal color to an RGB color. Credit:
     * http://stackoverflow.com/questions/5623838
     */
    function hexToRgb(hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    function plotPCA(pcaObj) {
        if (typeof pcaObj === 'undefined')
            return;

        // If there is only one data series, use Geneva's blue. Otherwise,
        // let Highcharts figure it out.
        if (pcaObj.series.length == 1) {
            Highcharts.setOptions({
                colors: ['#1689E5']
            });
        }

        var tooltipFormatter = function() { return this.key; },
            mins = pcaObj.ranges[1],
            maxs = pcaObj.ranges[0],
            titles = pcaObj.titles,
            chart;

        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'pca-plot',
                margin: [150, 150, 150, 150],
                type: 'scatter',
                options3d: {
                    enabled: true,
                    alpha: 20,
                    beta: 30,
                    depth: 500
                }
            },
            legend: {
                floating: true,
                layout: 'vertical',
                align: 'left',
                verticalAlign: 'top'
            },
            title: {
                text: '3D PCA plot'
            },
            subtitle: {
                text: 'using x y z coordinates'
            },
            xAxis: {
                title: {text: titles[0]},
                min: mins[0],
                max: maxs[0]
            },
            yAxis: {
                title: {text: titles[1]},
                min: mins[1],
                max: maxs[1]
            },
            zAxis: {
                title: {text: titles[2]},
                min: mins[2],
                max: maxs[2]
            },
            series: pcaObj.series,
            tooltip: {
                formatter: tooltipFormatter,
                useHTML: true,
                backgroundColor: '#7FB800', // green
                borderColor: '#7FB800',
                borderRadius: 0,
                shadow: false,
                style: {
                    color: 'white',
                    fontFamily: 'Roboto',
                    fontWeight: 'bold',
                    padding: 6
                }
            }
        });

        // Add mouse events for rotation
        $(chart.container).bind('mousedown.hc touchstart.hc', function (e) {
            e = chart.pointer.normalize(e);

            var posX = e.pageX,
                posY = e.pageY,
                alpha = chart.options.chart.options3d.alpha,
                beta = chart.options.chart.options3d.beta,
                newAlpha,
                newBeta,
                sensitivity = 5; // lower is more sensitive

            $(document).bind({
                'mousemove.hc touchdrag.hc': function (e) {
                    newBeta = beta + (posX - e.pageX) / sensitivity;
                    chart.options.chart.options3d.beta = newBeta;
                    newAlpha = alpha + (e.pageY - posY) / sensitivity;
                    chart.options.chart.options3d.alpha = newAlpha;
                    chart.redraw(false);
                },
                'mouseup touchend': function () {
                    $(document).unbind('.hc');
                }
            });
        });
    }

    function plotBar(barplotObj, renderTo) {
        var colors10 = ['#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9', 
        '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1'];

        var chart;
        var sortDataAndAddColor = function(data, attr){
            // array of objects sorted by attr, then add colors 
            data = _.sortBy(data, attr).reverse();
            var data_ = [];
            for (var i = 0; i < data.length; i++) {
                var obj = data[i]
                obj['color'] = colors10[i % 10];
                obj['y']  = obj[attr]
                data_.push(obj)
            };
            return data_;
        };

        var processAndSortData = function(data, attr){
            function fix_key(key){
                if (key.length === 1){
                    key = key + '_'
                }
                return key
            }
            var data_ = []
            for (var i = 0; i < data.length; i++) {
                var obj = data[i]
                var obj_ = _.object(
                    _.map(_.keys(obj), fix_key),
                    _.values(obj)
                    );
                data_.push(obj_)
            };
            data_ = sortDataAndAddColor(data_, attr);
            return data_;
        };

        var data = processAndSortData(barplotObj.data, 'x_');


        var tooltipFormatter = function() { 
            var value = this.point.y;
            if (value % 1 === 0){
                return '<table>' +
                        '<tr><th colspan="2"><h3>'+this.point.name+'</h3></th></tr>' +
                        '<tr><th>Co-occurence count:</th><td>'+value+'</td></tr>' +
                        '</table>'
            }else{
                value = Highcharts.numberFormat(value, 3);
                return '<table>' +
                        '<tr><th colspan="2"><h3>'+this.point.name+'</h3></th></tr>' +
                        '<tr><th>Jaccard Index:</th><td>'+value+'</td></tr>' +
                        '</table>'                
            }
        };

        chart = new Highcharts.Chart({
            chart: {
                renderTo: renderTo,
                type: 'column',
            },
            legend: {
                enabled: true,
            },
            title: {
                text: 'Bar plot'
            },
            xAxis: {
                type: 'category',
                labels: {
                    enabled: true
                },
            },
            yAxis: {
                allowDecimals: true,
                title: {
                    text: 'Jaccard Index'
                }
            },
            tooltip: {
                useHTML: true,
                formatter: tooltipFormatter,
            },
            series: [],
        });
        chart.addSeries({data: data})
        
        // button to switch data
        var btnSelector = '#'+ renderTo + '-btn';
        $(btnSelector).attr('currentAttr', 'x_');
        $(btnSelector).text('Sort by co-occurence count');

        $(btnSelector).click(function(){
            var currentAttr = $(this).attr('currentAttr');

            if (currentAttr == 'z_'){ // current is count, switch to rate
                $(btnSelector).text('Sort by co-occurence count');
                var data1 = processAndSortData(data, 'x_');
                
                chart.series[0].remove(false)
                chart.addSeries({data: data1}, false)
                chart.yAxis[0].setTitle({text:'Jaccard Index'}, false);
                chart.yAxis[0].setExtremes(0, data1[0].y, false);
                chart.yAxis[0].update({
                    'type': 'linear'
                });

                $(this).attr('currentAttr', 'x_')
            } else{ // current is rate, switch to count
                $(btnSelector).text('Sort by Jaccard Index');
                var data2 = sortDataAndAddColor(data, 'z_');

                chart.series[0].remove(false)
                chart.addSeries({data: data2}, false)
                chart.yAxis[0].setTitle({text:'Co-occurence count'}, false);
                chart.yAxis[0].setExtremes(0, data2[0].y, false);
                chart.yAxis[0].update({
                    'type': 'logarithmic'
                });

                $(this).attr('currentAttr', 'z_')
            }
        })
        
    }

    function plotBubble(bubbleObj, renderTo){
        var chart;
        var tooltipFormatter = function() { 
            var x = Highcharts.numberFormat(this.point.x, 4);
            return '<table>' +
                    '<tr><th colspan="2"><h3>'+this.point.name+'</h3></th></tr>' +
                    '<tr><th>Jaccard Index:</th><td>'+x+'</td></tr>' +
                    '<tr><th>Total count:</th><td>'+this.point.y+'</td></tr>' +
                    '<tr><th>Co-occurence count:</th><td>'+this.point.z+'</td></tr>' + 
                    '</table>'
        };

        chart = new Highcharts.Chart({
            chart: {
                renderTo: renderTo,
                type: 'bubble',
                zoomType: 'xy'
            },
            legend: {
                enabled: false,
            },
            title: {
                text: 'Bubble chart'
            },
            xAxis: {
                gridLineWidth: 1,
                title: {
                    text: 'Jaccard Index'
                },
                labels: {
                    enabled: true
                },
            },
            yAxis: {
                title: {
                    text: 'Total count'
                },
                labels: {
                    enabled: true
                },
            },
            tooltip: {
                useHTML: true,
                formatter: tooltipFormatter,
            },            
            plotOptions: {
                series: {
                    dataLabels: {
                        enabled: true,
                        format: '{point.name}'
                    },
                    colorByPoint: true
                }
            },
            series: [{
                data: bubbleObj['data']
            }]

        });
    }

    function plotKDE(kdeObj, renderTo){
        var chart;
        var tooltipFormatter = function() { 
            var y = Highcharts.numberFormat(this.point.y, 4);
            return '<table>' +
                    '<tr><th colspan="2"><h3>'+this.point.name+'</h3></th></tr>' +
                    '<tr><th>Co-occurence rate:</th><td>'+this.point.x+'</td></tr>' +
                    '<tr><th>Total count:</th><td>'+y+'</td></tr>' +
                    '<tr><th>Co-occurence count:</th><td>'+this.point.z+'</td></tr>' + 
                    '</table>'
        };
        
        chart = new Highcharts.Chart({
            chart: {
                renderTo: renderTo,
                type: 'area'
            },
            title: {
                text: 'Age distribution'
            },
            xAxis: {
                allowDecimals: false,
                title: {
                        text: 'Age (years)'
                },
                labels: {
                    formatter: function () {
                        return this.value;
                    }
                }
            },
            yAxis: {
                title: {
                    text: 'Probability'
                },
                labels: {
                    enabled: true
                }
            },
            tooltip: {
                    headerFormat: '',
                pointFormat: 'Probability: {point.y:,.3f}<br/>Age: {point.x:,.0f}'
            },
            plotOptions: {
                area: {
                    pointStart: kdeObj['age_years'][0],
                    pointInterval: kdeObj['age_years'][1] - kdeObj['age_years'][0],
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2,
                        states: {
                            hover: {
                                enabled: true
                            }
                        }
                    }
                }
            }, 
            series: [{
                name: kdeObj['name'],
                data: kdeObj['density']
            }]
        })        

    }

    /* Strip the preceding number, spaces, and hyphens from the names.
     */
    function cleanName(name) {
        return name.replace(/^[0-9]+ - /, '');
    }

    // For debugging.
    window.clustergrams = clustergrams;
}