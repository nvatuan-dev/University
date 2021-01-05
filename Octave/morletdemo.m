function morletdemo(noisy,freq,Fs,speed);


x = morse('CQ de AG1LE','CQ.wav',noisy,freq,Fs,speed);


w = 8;          %  peak will be at wavelet # w
Fo = freq / (Fs/w)     % tell wavelet transform where wavelet center frequency is 
sigma  = (1.2/speed)/w  % wavelet bandwidth - impacts time resolution


c = morlet(x',16,2,sigma,Fo);         % do Morlet wavelet transform
y = filter(ones(1,20)/20,1,c(w,:));   % y = low pass filter C(t,w) wavelet 
figure(4)
plot(y);                              % plot C(t,w) envelope


z = stft(x,1/Fs,4,128,1,512); % plot spectrogram of the signal using Short Term FFT 
end;
