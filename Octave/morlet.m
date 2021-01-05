
% Project 2
% Time-Frequency Representations
% Andy Doran, modified by  AG1LE Mauri Niininen 
% 
% function coeffs = cwvt(sigin,scale,quiet,sigma,fo)
%
% sigin  = sampled input signal (Should be a row vector)
% scale  = number of real, positive scale you want (1:scales)
% quiet  = plot suppression
%          1 -> suppress all plots
%          2 -> suppress wavelet plots only
%          3 -> suppress scalogram only
% sigma =0.015625;     Morlet Wavelet bandwidth
% fo = 0.25;           Center frequency of Wavelet
% coeffs = scales-by-length(sigin) matrix returning CWT of sigin at
%          each scale from 1 to scale
%
% This function takes an input signal and computes the Continuous Wavelet
% Transform at different scales using a sampled Morlet Wavelet
%
% Morelet Wavelet w(t) = (1/sigma*K)*exp-((sigma*t)^2)*cos(2*pi*fo*t)


function coeffs = morlet(sigin,scale,quiet,sigma,fo)




K = 1;           % Not sure what this is, so set to 1


M = length(sigin);
coeffs = zeros(scale,M);


for k=1:scale,
    t=(-M/2:M/2-1);


    % Calculate Morelet Wavelet w=e-(at^2)*cos(2*pi*fo*t)
    const = 1/(sigma*K*sqrt(k)); % k impacts relative amplitude
    e = exp(-((sigma*t).^2));    % removed k to keep the wavelet duration constant
    phase = cos(2*pi*fo*t/k);    % k impacts frequency 
    w = const*e.*phase;


    % Plot wavelet in time domain and frequency domain
    if ((quiet ~= 1) & (quiet ~= 2))
      figure(3)
      if (k == 1)  % Clear plot on initial run-through
        clf
      end
      subplot(scale,2,(2*k)-1)
      plot(w)
      txt = ['Modified Morlet Wavelet at scale ', num2str(k)];
      title(txt)
      %figure(4)
      %if (k == 1)  % Clear plot on initial run-through
      %  clf
      %end
      subplot(scale,2,2*k)
      plot(abs(fft(w)))
      txt = ['Frequency Spectra of Morlet Wavelet at scale ', num2str(k)];
      title(txt)
   end
    % Calculate CWT of sigin using circular convolution
%    coeffs(k,:)=ifft(fft(w).*fft(sigin));
    coeffs(k,:)=abs(fftshift(ifft(fft(w).*fft(sigin))));
end


% Coeffs should be real anyway, this just accounts for numerical error
% in circular convolution that may give small imaginary parts
coeffs = real(coeffs);


% Plot scalogram and check against MATLAB's CWT routine
if ((quiet ~= 1) & (quiet ~= 3))
  figure(1)
  %clf
  map = jet();
  colormap(map);
  imagesc(coeffs);
  axis xy;
  txt = ['abs|C(t,s)| for s = 1 to ' num2str(scale)];
  title(txt)
  ylabel('s')
  xlabel('t')
  figure(2);
  plot(sigin);  
  title('original signal');
 %figure(4);
  %clf
  %cwt(sigin,1:scale,'morl','plot');  % Call MATLAB's CWT routine
  %title('CWT Output from MATLAB')
end
