# AstroPi
<div class="document">

<div class="documentwrapper">

<div class="bodywrapper">

<div class="body" role="main">

<div class="section" id="astropi-docs">

# AstroPi docs(#astropi-docs "Permalink to this headline")

<span class="target" id="module-main"></span>

<dl class="class">

<dt id="main.Astro_Pi">_class_ `main.``Astro_Pi`<span class="sig-paren">(</span>_running_time_<span class="sig-paren">)</span>(#main.Astro_Pi "Permalink to this definition")</dt>

<dd>

Class for every function used in experiment (a way to order the code)

<dl class="method">

<dt id="main.Astro_Pi.calculate_force">`calculate_force`<span class="sig-paren">(</span><span class="sig-paren">)</span>(#main.Astro_Pi.calculate_force "Permalink to this definition")</dt>

<dd>

Calculating force and speed for the ISS @return: dict

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.check_sleep">`check_sleep`<span class="sig-paren">(</span>_timedelta_seconds_<span class="sig-paren">)</span>(#main.Astro_Pi.check_sleep "Permalink to this definition")</dt>

<dd>

Checks if can sleep or if the current_time + sleep_time exceeds project time @param1: int @return: Boolean

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.check_time">`check_time`<span class="sig-paren">(</span><span class="sig-paren">)</span>(#main.Astro_Pi.check_time "Permalink to this definition")</dt>

<dd>

Checks if the time for the experiment is up @return: Boolean

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.get_coordinates_ISS">`get_coordinates_ISS`<span class="sig-paren">(</span><span class="sig-paren">)</span>(#main.Astro_Pi.get_coordinates_ISS "Permalink to this definition")</dt>

<dd>

Get’s current ISS coordinates @return: dict

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.setup_logger">`setup_logger`<span class="sig-paren">(</span>_dir_path_, _name_<span class="sig-paren">)</span>(#main.Astro_Pi.setup_logger "Permalink to this definition")</dt>

<dd>

Tries to create csv logger object

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.show_country">`show_country`<span class="sig-paren">(</span><span class="sig-paren">)</span>(#main.Astro_Pi.show_country "Permalink to this definition")</dt>

<dd>

Gets the country that is below ISS @return: dict

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.show_country_countinously">`show_country_countinously`<span class="sig-paren">(</span><span class="sig-paren">)</span>(#main.Astro_Pi.show_country_countinously "Permalink to this definition")</dt>

<dd>

Updates the country flags on the SenseHat LED Matrix (every 5s)

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.write_data_continuously">`write_data_continuously`<span class="sig-paren">(</span>_files_<span class="sig-paren">)</span>(#main.Astro_Pi.write_data_continuously "Permalink to this definition")</dt>

<dd>

Writes humidity, temperature and pressure for the current time (every 60s) @return: None

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.write_data_csv">`write_data_csv`<span class="sig-paren">(</span>_file_<span class="sig-paren">)</span>(#main.Astro_Pi.write_data_csv "Permalink to this definition")</dt>

<dd>

Writes current data to the csv file

</dd>

</dl>

<dl class="method">

<dt id="main.Astro_Pi.write_force_csv">`write_force_csv`<span class="sig-paren">(</span>_file_<span class="sig-paren">)</span>(#main.Astro_Pi.write_force_csv "Permalink to this definition")</dt>

<dd>

Writes the force and speed data to the designated csv file

</dd>

</dl>

</dd>

</dl>

</div>

</div>

</div>

</div>
<div class="footer">©2020 Authors: Raducu Alexandru Mircea, Mocanu Alexandru, Negrea Mihail Daniel, Stancu Vlad, Ioana Stoica.</div>
