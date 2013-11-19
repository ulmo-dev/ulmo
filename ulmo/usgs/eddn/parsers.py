from datetime import timedelta
import pandas as pd


def twdb_stevens(dataframe, drop_dcp_metadata=True):
    """Parser for twdb stevens dataloggers.
    Data is transmitted every 12 hours and each message contains 12 water level measurements on the hour
    for the previous 12 hours and one battery voltage measurement for the current hour

    format examples:

    '"BV:12.5  451.70$ 451.66$ 451.66$ 451.62$ 451.59$ 451.57$ 451.54$ 451.53$ 451.52$ 451.52$ 451.52$ 451.52$ '
    '"BV:12.2  Channel:5 Time:43 +441.48 +443.25 +440.23 +440.67 +441.26 +441.85 +442.66 +443.84 +445.24 +442.15 +442.88 +443.91 '
    '"BV:12.6  Channel:5 Time:28 +304.63 +304.63 +304.63 +304.56 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.71 Channel:6 Time:28 +310.51 +310.66 +310.59 +310.51 +310.51 +310.59 +310.59 +310.51 +310.66 +310.51 +310.66 +310.59 '
    """
    message = dataframe['dcp_message'].lower()
    message_timestamp = dataframe['message_timestamp_utc']

    fields = message.split()
    battery_voltage = fields[0].split(':')[-1]
    message = ' '.join(fields[1:])
    fmt = '$+-"\x7f '

    df = []
    if 'channel' in message:
        for channel_msg in message.strip('channel:').split('channel:'):
            fields = channel_msg.split()
            msg_channel = fields[0].split(':')[-1]
            msg_time = fields[1].split(':')[-1]
            water_levels = [field.strip(fmt) for field in fields[2:]]
            data = _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels)
            data['channel'] = msg_channel
            data['time'] = msg_time
            df.append(data)
    else:
        fields = message.split()
        water_levels = [field.strip(fmt) for field in fields]
        data = _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels)
        df.append(data)

    df = pd.concat(df)

    if not drop_dcp_metadata:
        for col in dataframe.index:
            df[col] = dataframe[col]

    return df


def twdb_sutron(dataframe, drop_dcp_metadata=True):
    """Parser for twdb sutron dataloggers.
    Data is transmitted every 12 hours and each message contains 12 water level measurements on the hour
    for the previous 12 hours and one battery voltage measurement for the current hour

    format examples:

    '":ott 60 #60 -190.56 -190.66 -190.69 -190.71 -190.74 -190.73 -190.71 -190.71 -190.71 -190.71 -190.72 -190.72 :BL 13.05  '
    '":SENSE01 60 #60 -82.19 -82.19 -82.18 -82.19 -82.19 -82.22 -82.24 -82.26 -82.27 -82.28 -82.28 -82.26 :BL 12.41  '
    '":OTT 703 60 #60 -231.47 -231.45 -231.44 -231.45 -231.47 -231.50 -231.51 -231.55 -231.56 -231.57 -231.55 -231.53 :6910704 60 #60 -261.85 -261.83 -261.81 -261.80 -261.81 -261.83 -261.85 -261.87 -261.89 -261.88 -261.86 -261.83 :BL 13.21'
    '":Sense01 10 #10 -44.70 -44.68 -44.66 -44.65 -44.63 -44.61 -44.60 -44.57 -44.56 -44.54 -44.52 -44.50 :BL 13.29'
    '"\r\n-101.11 \r\n-101.10 \r\n-101.09 \r\n-101.09 \r\n-101.08 \r\n-101.08 \r\n-101.08 \r\n-101.10 \r\n-101.11 \r\n-101.09 \r\n-101.09 \r\n-101.08'
    '"\r\n// \r\n// \r\n// \r\n// \r\n// \r\n-199.88 \r\n-199.92 \r\n-199.96 \r\n-199.98 \r\n-200.05 \r\n-200.09 \r\n-200.15'
    '":Sense01 60 #60 M M M M M M M M M M M M :BL 12.65'
    """
    message = dataframe['dcp_message'].lower()
    message_timestamp = dataframe['message_timestamp_utc']

    lines = message.strip('":').split(':')
    if len(lines) == 1:
        water_levels = [field.strip('+- ') for field in lines[0].split()]
        df = _twdb_assemble_dataframe(message_timestamp, None, water_levels)
    else:
        data = []
        battery_voltage = lines[-1].split('bl')[-1].strip()
        for line in lines[:-1]:
            channel = line[:7]
            split = line[7:].split()
            water_levels = [field.strip('+-" ') for field in split[2:]]
            df = _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels)
            df['channel'] = channel
            data.append(df)
        df = pd.concat(data)

    if not drop_dcp_metadata:
        for col in dataframe.index:
            df[col] = dataframe[col]

    return df


def twdb_texuni(dataframe, drop_dcp_metadata=True):
    """Parser for twdb texuni dataloggers.
    Data is transmitted every 12 hours and each message contains 12 water level measurements on the hour
    for the previous 12 hours

    format examples:
    '"\r\n+0.000,-245.3,\r\n+0.000,-245.3,\r\n+0.000,-245.3,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.5,\r\n+0.000,-245.5,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+412.0,+2013.,+307.0,+1300.,+12.75,+0.000,-245.4,-245.3,-245.6,+29.55,'
    ' \r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+340.0,+2013.,+307.0,+1400.,+12.07,+0.000,-109.9,-109.8,-110.1,+30.57,'
    """

    message = dataframe['dcp_message']
    message_timestamp = dataframe['message_timestamp_utc']
    water_levels = [row.split(',')[1].strip('+- ') for row in message.strip('" \r\n').splitlines()[:-1]]

    df = _twdb_assemble_dataframe(message_timestamp, None, water_levels)

    if not drop_dcp_metadata:
        for col in dataframe.index:
            df[col] = dataframe[col]

    return df


def _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels):
    data = []
    base_timestamp = message_timestamp.replace(minute=0, second=0, microsecond=0)
    water_levels.reverse()
    try:
        battery_voltage = float(battery_voltage)
    except:
        battery_voltage = pd.np.nan

    for hrs, water_level in enumerate(water_levels):
        timestamp = base_timestamp - timedelta(hours=hrs)
        try:
            water_level = float(water_level)
        except:
            water_level = pd.np.nan

        if hrs==0 and battery_voltage:
            data.append([timestamp, battery_voltage, water_level])
        else:
            data.append([timestamp, pd.np.nan, water_level])

    df = pd.DataFrame(data, columns=['timestamp_utc', 'battery_voltage', 'water_level'])
    df.index = pd.to_datetime(df['timestamp_utc'])
    del df['timestamp_utc']
    return df
