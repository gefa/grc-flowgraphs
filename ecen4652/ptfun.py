#!/usr/bin/env python3
# File: ptfun
# Functions for gnuradio-companion PAM p(t) generation
import numpy as np

def pampt(sps, ptype, pparms=[]):
    """
    PAM pulse p(t) = p(n*TB/sps) generation
    >>>>> pt = pampt(sps, ptype, pparms) <<<<<
    where  sps:
        ptype: pulse type (’rect’, ’sinc’, ’tri’)
        pparms not used for ’rect’, ’tri’
        pparms = [k, beta] for sinc
        k:     "tail" truncation parameter for ’sinc’
            (truncates p(t) to -k*sps <= n < k*sps)
        beta:  Kaiser window parameter for ’sinc’
        pt:    pulse p(t) at t=n*TB/sps
    Note: In terms of sampling rate Fs and baud rate FB,
        sps = Fs/FB
    """
    if ptype.lower()=='man':
        nn=np.arange(np.ceil(-sps/2.0),np.ceil(sps/2.0))
        PAMpn=-np.ones(len(nn))
        ix=np.where(nn>=0)[0]
        PAMpn[ix]=1
    elif ptype.lower()=='msin':
        nn=np.arange(np.ceil(-sps/2.0),np.ceil(sps/2.0))
        PAMpn=np.sin(2*np.pi*nn/float(sps))
    elif ptype.lower()=='rect':
        nn=np.arange(0,sps)
        PAMpn=np.ones(len(nn))
    elif ptype.lower()=='tri':
        nn=np.arange(-sps,sps)
        PAMpn=1+nn/float(sps)
        ix=np.where(nn>=0)[0]
        PAMpn[ix]=1-nn[ix]/float(sps)
    elif ptype.lower()=='sinc':
        k=5# default k
        if len(pparms)>0:
            k=pparms[0]
        nn=np.arange(-k*sps,k*sps)
        PAMpn=np.sinc(nn/float(sps))
        if len(pparms)>1:
            PAMpn=PAMpn*np.kaiser(len(PAMpn),pparms[1])
    elif ptype.lower()=='rcf':
        k=5# default k
        if len(pparms)>0:
            k=pparms[0]
        nn=np.arange(-k*sps,k*sps)
        PAMpn=np.sinc(nn/float(sps))
        alfa=0.3
        if len(pparms)>1:
            alfa=pparms[1]
        if alfa!=0:
            PAMp2n=np.pi/4.0*np.ones(PAMpn.size)
            ix=np.where(np.power(2*alfa*nn/float(sps),2.0)!=1)[0]
            PAMp2n[ix]=np.cos(np.pi*alfa*nn[ix]/float(sps))
            PAMp2n[ix]=PAMp2n[ix]/(1-np.power(2*alfa*nn[ix]/float(sps),2.0))
            PAMpn=PAMpn*PAMp2n
    elif ptype.lower()=='rrcf':
        k=5# default k
        if len(pparms)>0:
            k=pparms[0]
        nn=np.arange(-k*sps,k*sps)
        alfa=0.3
        if len(pparms)>1:
            alfa=pparms[1]
        PAMpn=(1-alfa+4*alfa/np.pi)*np.ones(len(nn))

    return PAMpn