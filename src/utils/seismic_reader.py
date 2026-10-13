import struct
import numpy as np



def write_seg2(data,fs,delay,source_pos,rec_location,name):

    rows,cols = np.shape(data)
    smrate = 1/fs

    # Default parameters from segy format as indicated in segymat
    group_x = np.zeros((cols))
    cdp = group_x
    cdp_trace = group_x
    energy_source_point = group_x + source_pos
    source_x = group_x
    field_record = group_x
    delay_recording_time = group_x + delay
    #rec_location = group_x


    with open(fr'{name}.dat','wb+') as fid:

        # Prepare Strings for File Descriptor Block
        fds1='TRACE_SORT AS_ACQUIRED'                    #File Descriptor String 1
        fds2='UNITS METERS'                              #File Descriptor String 2


        #Next statement calculates the combined length of strings including the two
        #empty bytes required at the end of the string sub-block to mark the end
        fdslen=len(fds1)+3+len(fds2)+3+2

        #Next line checks how many bytes are needed to pad block to a division of 4
        fdspad=4-((fdslen)/4-np.floor((fdslen)/4))/0.25

        #Next statement is needed because if tspad==4 then there is no need to pad
        if fdspad==4: 
            fdspad=0 

        # Prepare Strings for Trace Descriptor Block
        # This section estimates the lengths of each string in the Trace
        # Descriptor Block and assigns an initial value

        tds = {'DELAY ':[],'RECEIVER_LOCATION ':[],'SAMPLE_INTERVAL ':[],'CDP_NUMBER ':[],
            'CDP_TRACE ':[],'RECEIVER_GEOMETRY ':[],'SHOT_SEQUENCE_NUMBER ':[],'SOURCE_LOCATION ':[],
            'SOURCE_GEOMETRY ':[],'SOURCE_STATION_NUMBER ':[],'CHANNEL_NUMBER ':[],'RAW_RECORD ':[],
            'SOURCE VIBROSEIS':['']}

        tds['DELAY ']=[("%8.4f"%(delay_recording_time[0]))]
        tds['RECEIVER_LOCATION ']=[("%15.3f"%(rec_location[0]))]
        tds['SAMPLE_INTERVAL ']=[("%0.6f"%(smrate))]
        tds['CDP_NUMBER ']=[("%08d"%(cdp[0]))]
        tds['CDP_TRACE ']=[("%08d"%(cdp_trace[0]))]
        tds['RECEIVER_GEOMETRY ']=[("%15.3f"%(group_x[0]))]
        tds['SHOT_SEQUENCE_NUMBER ']=[("%08d"%(energy_source_point[0]))]
        tds['SOURCE_LOCATION ']=[("%15.3f"%(energy_source_point[0]))]
        tds['SOURCE_GEOMETRY ']=[("%15.3f"%(source_x[0]))]
        tds['SOURCE_STATION_NUMBER ']=[("%08d"%(source_x[0]))]
        tds['CHANNEL_NUMBER ']=[("%08d"%(cdp_trace[0]))]
        tds['RAW_RECORD ']=[("%08d"%(field_record[0]))]
        tds['SOURCE VIBROSEIS']


        #Next statement calculates the combined length of strings including the two
        #empty bytes required at the end of the string sub-block to mark the end

        lr = [len(list(tds.keys())[ik] + tds[list(tds.keys())[ik]][0]) for ik in range(len(tds))]

        tdslen=sum(lr)+3*len(tds)+2

        #%Next line checks how many bytes are needed to pad block to a division of 4
        tdspad=4-((tdslen/4)-np.floor((tdslen)/4))/0.25 

        #% Next statement is needed because if tspad==4 then there is no need to pad
        if tdspad==4: 
            tdspad=0 


        #% Write FILE DESCRIPTOR BLOCK

        uint16 = '<H'
        uint8 = '<B'
        ulong = '<L'
        float32 = '<f'

        fid.write(struct.pack(uint16, int('3A55',base=16)))
        fid.write(struct.pack(uint16, 1))
        fid.write(struct.pack(uint16, cols*4))
        fid.write(struct.pack(uint16, cols))
        fid.write(struct.pack(uint8, int('01',base=16)))
        fid.write(struct.pack(uint8, 0))
        fid.seek(fid.tell()+1,0)
        fid.write(struct.pack(uint8, int('02',base=16)))
        fid.write(struct.pack(uint8, int('0A',base=16)))
        fid.write(struct.pack(uint8, int('0D',base=16)))


        #print(fid.read())
        for i in range(1,cols+1):
            if i==1: #% When c==1 the pointer skips over the RESERVED Bytes
                fid.seek(fid.tell()+18,0)
                fid.write(struct.pack(ulong, int(32+(4*(cols))+fdslen+fdspad+((32+tdslen+tdspad+(rows*4))*(i-1)))))
            else:  #%Writes byte location of remaining trace pointer sub-blocks
                fid.write(struct.pack(ulong, int(32+(4*(cols))+fdslen+fdspad+((32+tdslen+tdspad+(rows*4))*(i-1)))))

        # Write Strings for File Descriptor block
        # Write TRACE_SORT string
        fid.write(struct.pack(uint16, int(len(fds1)+3)))
        fid.write(struct.pack(fr'<{len(fds1)}s', bytes(fds1,"utf-8")))
        fid.write(struct.pack(uint8, 0))
        fid.write(struct.pack(uint16, int(len(fds2)+3)))
        fid.write(struct.pack(fr'<{len(fds2)}s', bytes(fds2,"utf-8")))
        fid.write(struct.pack(uint8, 0))

        # Write TRACE DESCRIPTOR and DATA BLOCK loops

        for i in range(cols):

            tds['DELAY ']=[("%8.4f"%(delay_recording_time[i]))]
            tds['RECEIVER_LOCATION ']=[("%15.3f"%(rec_location[i]))]
            tds['SAMPLE_INTERVAL ']=[("%0.6f"%(smrate))]
            tds['CDP_NUMBER ']=[("%08d"%(cdp[i]))]
            tds['CDP_TRACE ']=[("%08d"%(cdp_trace[i]))]
            tds['RECEIVER_GEOMETRY ']=[("%15.3f"%(group_x[i]))]
            tds['SHOT_SEQUENCE_NUMBER ']=[("%08d"%(energy_source_point[i]))]
            tds['SOURCE_LOCATION ']=[("%15.3f"%(energy_source_point[i]))]
            tds['SOURCE_GEOMETRY ']=[("%15.3f"%(source_x[i]))]
            tds['SOURCE_STATION_NUMBER ']=[("%08d"%(source_x[i]))]
            tds['CHANNEL_NUMBER ']=[("%08d"%(cdp_trace[i]))]
            tds['RAW_RECORD ']=[("%08d"%(field_record[i]))]
            tds['SOURCE VIBROSEIS']


            if i==0:
                skip=2+fdspad #Number of bytes to skip to ensure file descriptor
                            #block is a division of 4
            else:
                skip=0 # No skipping is required one first byte of Trace descriptor
                        #block has been written

            fid.seek(int(fid.tell()+skip),0)
            fid.write(struct.pack(uint16, int('4422',base=16)))
            fid.write(struct.pack(uint16, int(32+tdslen+tdspad)))
            fid.write(struct.pack(ulong,int(4*rows)))
            fid.write(struct.pack(ulong,int(rows)))
            fid.write(struct.pack(uint8, int('04',base=16)))


            for k in range(len(tds)):

                par_name = list(tds.keys())[k] + tds[list(tds.keys())[k]][0]

                if k==0:
                    skip=19
                else:
                    skip=0
                
                fid.seek(fid.tell()+skip,0)
                fid.write(struct.pack(uint16, int(len(par_name)+3)))
                fid.write(struct.pack(fr'<{len(par_name)}s', bytes(par_name,"utf-8")))
                fid.write(struct.pack(uint8, 0))


            for j in range(rows):
                if j==0:
                    fid.seek(int(fid.tell()+2+tdspad),0)
                    fid.write(struct.pack(float32, data[j,i]))
                else:
                    fid.write(struct.pack(float32, data[j,i]))

    fid.close()




