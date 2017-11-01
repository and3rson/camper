Components
===========

Input channel hierarchy
-----------------------

.. graphviz::

    digraph A {
        node[shape="box", style="filled", fontname="sans-serif", color="navy", fillcolor="blue", fontcolor="white"];
        edge[color="darkgreen"];
        subgraph cluster_0 {
            label = "Channels";
            fontname = "sans-serif";
            channel1[label="Input channel"];
            channel2[label="Input channel"];
        }
        subgraph cluster_1 {
            label = "Values";
            fontname = "sans-serif";
            value1[label="Value"];
            value2[label="Value"];
            value3[label="Value"];
            value4[label="Value"];
            value5[label="Value"];
        }
        subgraph cluster_2 {
            label = "Things";
            fontname = "sans-serif";
            thing1[label="Thing"];
            thing2[label="Thing"];
        }
        sensor1 [label="Light sensor"];
        sensor2 [label="Temperature sensor"];
        sensor3 [label="Humidity sensor"];
        device1 [label="e.g. Arduino"];
        device2 [label="e.g. ESP8266"];
        sensor1 -> device1;
        sensor2 -> device2;
        sensor3 -> device2;
        device1 -> channel1;
        device2 -> channel2;
        channel1 -> value1;
        channel1 -> value2;
        channel1 -> value3;
        channel2 -> value4 [color="gold3"];
        channel2 -> value5 [color="gold3"];
        value1 -> thing1;
        value2 -> thing1;
        value3 -> thing1;
        value4 -> thing2 [color="gold3"];
        value5 -> thing2 [color="gold3"];
    }

Input channels
--------------

:term:`Input channel` represents a router for incoming data.

It is preferred to have one input channel per physical microcontroller.

:term:`Input channel` has ID and public URL that can be used to push data to this channel.

At the time being, only push method is supported. In future, polling input channels will be implemented.

:term:`Input channel` can have multiple values attached.

Values
------

:term:`Value` represents a scalar value received via input channel.

It has a single :term:`Input channel` it relates to, although :term:`Input channel` may (and typically would) have multiple associated :term:`Value` instances.

:term:`Value` defines a portion of data that was received via an :term:`Input channel`. Data is extracted from :term:`Input channel` based on the json_path rule of the :term:`Value`.

Typical example would be to post "temperature" and "humidity" data to an :term:`Input channel`. This data can then be extracted into two :term:`Value` instances.

:term:`Value` can be "alive" or "dead" based on the ttl_seconds parameter.

:term:`Value` can belong to multiple :term:`Thing` instances.

Things
------

:term:`Thing` represents a composition of :term:`Value` instances.

:term:`Thing` may have multiple :term:`Value` instances associated with it, and :term:`Value` can belong to multiple :term:`Thing` instances.

:term:`Thing` inherits its "alive" status from associated :term:`Value` instances. If any associated :term:`Value` changes its state to "dead", then all :term:`Thing` instances that reference it are also marked as "dead".

:term:`Thing` becomes alive once all corresponding :term:`Value` instances go "alive".

