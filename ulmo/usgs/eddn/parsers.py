from datetime import datetime, timedelta
import pandas as pd


def twdb_stevens(dataframe, drop_dcp_metadata=True):
    # '"BV:12.5  451.70$ 451.66$ 451.66$ 451.62$ 451.59$ 451.57$ 451.54$ 451.53$ 451.52$ 451.52$ 451.52$ 451.52$ '
    # '"BV:12.2  Channel:5 Time:43 +441.48 +443.25 +440.23 +440.67 +441.26 +441.85 +442.66 +443.84 +445.24 +442.15 +442.88 +443.91 '
    # '"BV:12.6  Channel:5 Time:28 +304.63 +304.63 +304.63 +304.56 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.71 Channel:6 Time:28 +310.51 +310.66 +310.59 +310.51 +310.51 +310.59 +310.59 +310.51 +310.66 +310.51 +310.66 +310.59 '    
    message = dataframe['dcp_message'].lower()
    message_timestamp = dataframe['message_timestamp_utc']

    fields = message.split()
    battery_voltage = fields[0].split(':')[-1]
    message = ' '.join(fields[1:])

    df = []
    if 'channel' in message:
        for channel_msg in message.strip('channel:').split('channel:'):
            fields = channel_msg.split()
            msg_channel = fields[0].split(':')[-1]
            msg_time = fields[1].split(':')[-1]
            water_levels = [field.strip('$+-" ') for field in fields[2:]]
            data = _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels)
            data['channel'] = msg_channel
            data['time'] = msg_time
            df.append(data)
    else:
        fields = message.split()
        water_levels = [field.strip('$+-" ') for field in fields]
        data = _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels)
        df.append(data)

    df = pd.concat(df)

    if not drop_dcp_metadata:
        for col in dataframe.index:
            df[col] = dataframe[col]

    return df


def twdb_sutron_linear(dataframe, drop_dcp_metadata=True):
    # '":ott 60 #60 -190.56 -190.66 -190.69 -190.71 -190.74 -190.73 -190.71 -190.71 -190.71 -190.71 -190.72 -190.72 :BL 13.05  '
    # '":SENSE01 60 #60 -82.19 -82.19 -82.18 -82.19 -82.19 -82.22 -82.24 -82.26 -82.27 -82.28 -82.28 -82.26 :BL 12.41  '

    message = dataframe['dcp_message'].lower()
    split = data.split()
    battery_voltage = split[-1] 
    water_levels = [field.strip('$+-" ') for field in split[3:-2]]
    df = _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels)    
    
    if not drop_dcp_metadata:
        for col in dataframe.index:
            df[col] = dataframe[col]

    return df


def _twdb_assemble_dataframe(message_timestamp, battery_voltage, water_levels):
    data = []
    base_timestamp = message_timestamp.replace(minute=0, second=0, microsecond=0)
    water_levels.reverse()

    for hrs, water_level in enumerate(water_levels):
        timestamp = base_timestamp - timedelta(hours=hrs)
        if hrs==0:
            data.append([timestamp, battery_voltage, water_level])
        else:
            data.append([timestamp, '', water_level])

    df = pd.DataFrame(data, columns=['timestamp_utc', 'battery_voltage', 'water_level'])
    df.index = pd.to_datetime(df['timestamp_utc'])
    del df['timestamp_utc']
    return df
