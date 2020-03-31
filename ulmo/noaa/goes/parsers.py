from datetime import timedelta
import pandas as pd
import numpy as np

battery_names = ['bl', 'vb', 'bv']


def twdb_dot(df_row, drop_dcp_metadata=True):
    """Parser for twdb DOT dataloggers."""
    return _twdb_stevens_or_dot(df_row, reverse=False,
                                drop_dcp_metadata=drop_dcp_metadata)


def twdb_fts(df_row, drop_dcp_metadata=True):
    """Parser for twdb fts dataloggers

    format examples:
    C510D20018036133614G39-0NN170WXW00097  :WL 31 #60 -72.91 -72.89 -72.89 -72.89 -72.91 -72.92 -72.93 -72.96 -72.99 -72.97 -72.95 -72.95
    """

    message = df_row['dcp_message'].lower()
    invalid_messages = ['dadds', 'operator', 'no']
    for invalid in invalid_messages:
        if invalid in message:
            df = _twdb_assemble_dataframe(
                df_row['message_timestamp_utc'], [np.nan], [np.nan]
            )
            return(df)
    message_timestamp = df_row['message_timestamp_utc']
    water_levels = [np.nan]
    battery_voltage = np.nan
    for line in message.split(':'):
        if line.split() != []:
            line = line.split()
            # grab water level data
            if line[0] == 'wl':
                water_levels = [
                    field.strip('+- ') for field in line[3:]
                ]
            # grab battery voltage
            if line[0] == 'vb':
                battery_voltage = line[3].strip('+- ')

    df = _twdb_assemble_dataframe(
        message_timestamp, battery_voltage, water_levels, reverse=False
    )

    if not drop_dcp_metadata:
        for col in df_row.index:
            df[col] = df_row[col]

    return df


def twdb_stevens(df_row, drop_dcp_metadata=True):
    """Parser for twdb stevens dataloggers."""
    return _twdb_stevens_or_dot(df_row, reverse=True,
                                drop_dcp_metadata=drop_dcp_metadata)


def twdb_sutron(df_row, drop_dcp_metadata=True):
    """Parser for twdb sutron dataloggers.
    Data is transmitted every 12 hours and each message contains 12 water level
    measurements on the hour for the previous 12 hours and one battery voltage
    measurement for the current hour

    format examples:

    '":ott 60 #60 -190.56 -190.66 -190.69 -190.71 -190.74 -190.73 -190.71 -190.71 -190.71 -190.71 -190.72 -190.72 :BL 13.05  '
    '":SENSE01 60 #60 -82.19 -82.19 -82.18 -82.19 -82.19 -82.22 -82.24 -82.26 -82.27 -82.28 -82.28 -82.26 :BL 12.41  '
    '":OTT 703 60 #60 -231.47 -231.45 -231.44 -231.45 -231.47 -231.50 -231.51 -231.55 -231.56 -231.57 -231.55 -231.53 :6910704 60 #60 -261.85 -261.83 -261.81 -261.80 -261.81 -261.83 -261.85 -261.87 -261.89 -261.88 -261.86 -261.83 :BL 13.21'
    '":Sense01 10 #10 -44.70 -44.68 -44.66 -44.65 -44.63 -44.61 -44.60 -44.57 -44.56 -44.54 -44.52 -44.50 :BL 13.29'
    '"\r\n-101.11 \r\n-101.10 \r\n-101.09 \r\n-101.09 \r\n-101.08 \r\n-101.08 \r\n-101.08 \r\n-101.10 \r\n-101.11 \r\n-101.09 \r\n-101.09 \r\n-101.08'
    '"\r\n// \r\n// \r\n// \r\n// \r\n// \r\n-199.88 \r\n-199.92 \r\n-199.96 \r\n-199.98 \r\n-200.05 \r\n-200.09 \r\n-200.15'
    '":Sense01 60 #60 M M M M M M M M M M M M :BL 12.65'
    """
    message = df_row['dcp_message'].strip().lower()
    if 'dadds' in message:
        return pd.DataFrame()

    message_timestamp = df_row['message_timestamp_utc']
    lines = message.strip('":').split(':')
    data = []
    for line in lines:
        split = line.split(' ')
        channel = split[0]
        if channel.lower() in battery_names:
            channel_data = [field.strip('+-" ') for field in split]
        else:
            channel_data = [field.strip('+-" ') for field in split[3:]]

        df = _twdb_assemble_dataframe(
            message_timestamp, channel, channel_data, reverse=False
        )
        data.append(df)
    df = pd.concat(data)

    if not drop_dcp_metadata:
        for col in df_row.index:
            df[col] = df_row[col]

    return df


def twdb_texuni(dataframe, drop_dcp_metadata=True):
    """Parser for twdb texuni dataloggers.
    Data is transmitted every 12 hours and each message contains 12 water level
    measurements on the hour for the previous 12 hours

    format examples:
    '"\r\n+0.000,-245.3,\r\n+0.000,-245.3,\r\n+0.000,-245.3,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.4,\r\n+0.000,-245.5,\r\n+0.000,-245.5,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+0.000,-245.6,\r\n+412.0,+2013.,+307.0,+1300.,+12.75,+0.000,-245.4,-245.3,-245.6,+29.55,'
    ' \r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+340.0,+2013.,+307.0,+1400.,+12.07,+0.000,-109.9,-109.8,-110.1,+30.57,'
    """

    message = dataframe['dcp_message']
    message_timestamp = dataframe['message_timestamp_utc']
    water_levels = [row.split(',')[1].strip('+- ') for
                    row in message.strip('" \r\n').splitlines()[:-1]]

    df = _twdb_assemble_dataframe(
        message_timestamp, None, water_levels, reverse=True
    )

    if not drop_dcp_metadata:
        for col in dataframe.index:
            df[col] = dataframe[col]

    return df


def _twdb_assemble_dataframe(message_timestamp, channel, channel_data,
                             reverse=False):
    data = []
    base_timestamp = message_timestamp.replace(
        minute=0, second=0, microsecond=0
    )
    if reverse:
        data.reverse()

    for hrs, value in enumerate(channel_data):
        timestamp = base_timestamp - timedelta(hours=hrs)
        try:
            value = float(value)
        except Exception:
            value = np.nan

        data.append([timestamp, channel, value])
    if len(data) > 0:
        df = pd.DataFrame(
            data, columns=['timestamp_utc', 'channel', 'channel_data']
        )
        df.index = pd.to_datetime(df['timestamp_utc'])
        del df['timestamp_utc']
        return df
    else:
        return pd.DataFrame()


def _twdb_stevens_or_dot(df_row, reverse, drop_dcp_metadata=True):
    """Parser for twdb stevens and DOT dataloggers - the only difference being
    that with stevens dataloggers, water level data needs to be reversed to be
    correctly interpretted.

    Data is transmitted every 12 hours and each message contains 12 water level
    measurements on the hour for the previous 12 hours and one battery voltage
    measurement for the current hour

    format examples:

    '"BV:12.5  451.70$ 451.66$ 451.66$ 451.62$ 451.59$ 451.57$ 451.54$ 451.53$ 451.52$ 451.52$ 451.52$ 451.52$ '
    '"BV:12.2  Channel:5 Time:43 +441.48 +443.25 +440.23 +440.67 +441.26 +441.85 +442.66 +443.84 +445.24 +442.15 +442.88 +443.91 '
    '"BV:12.6  Channel:5 Time:28 +304.63 +304.63 +304.63 +304.56 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.71 Channel:6 Time:28 +310.51 +310.66 +310.59 +310.51 +310.51 +310.59 +310.59 +310.51 +310.66 +310.51 +310.66 +310.59 '
    """
    message = df_row['dcp_message'].strip().lower()
    if 'dadds' in message or 'operator' in message or 'no' in message:
        return(pd.DataFrame())

    message_timestamp = df_row['message_timestamp_utc']

    data = []
    # this should really be it's own parser...
    if df_row['dcp_address'] in ['C51CB67A']:
        fields = message.strip('" \x10\x00').split('\r')
        channel_data = {}
        channel_data['bv'] = [fields[0].split(':')[1].split()[0]]
        for field in fields[1:]:
            df = pd.DataFrame()
            try:
                channel, channel_datum = field.strip('\n').split(': ')
                if channel in channel_data:
                    channel_data[channel].append(channel_datum.strip('+-'))
                else:
                    channel_data[channel] = [channel_datum.strip('+-')]
            except Exception:
                pass

        for channel in channel_data:
            df = _twdb_assemble_dataframe(
                message_timestamp, channel, channel_data[channel],
                reverse=reverse
            )
            data.append(df)

        df = pd.concat(data)
        if not drop_dcp_metadata:
            for col in df_row.index:
                df[col] = df_row[col]

        return df

    fields = message.strip('" ').split()

    water_channel = 'wl'
    water_data = {}
    for field in fields:
        df = pd.DataFrame()
        if field[:2].lower() in battery_names:
            channel, channel_data = field.lower().split(':')
            channel_data = [channel_data]
            df = _twdb_assemble_dataframe(
                message_timestamp, channel, channel_data, reverse=reverse
            )
        elif 'time' in field.lower():
            channel, channel_data = field.lower().split(':')
            channel_data = [channel_data]
            df = _twdb_assemble_dataframe(
                message_timestamp, channel, channel_data, reverse=reverse
            )
        elif 'channel' in field.lower():
            cnum = field.lower().split(':')[1]
            if cnum not in water_data:
                water_data[cnum] = []
        else:
            try:
                water_data[cnum].append(float(field.strip('+-$')))
            except Exception:
                pass
        data.append(df)

    for channel in water_data: 
        data.append(
            _twdb_assemble_dataframe(
                message_timestamp, channel, water_data[channel], reverse=reverse
            )
        )
    df = pd.concat(data)

    if not drop_dcp_metadata:
        for col in df_row.index:
            df[col] = df_row[col]

    return df


def _parse_value(water_level_str):
    well_val = water_level_str.split(':')
    if len(water_level_str.split(':')) == 2:
        if well_val[1] == '':
            val = np.nan
        else:
            val = well_val[1].strip('-')
        value_dict = (well_val[0], val)
        return value_dict
    else:
        return water_level_str
