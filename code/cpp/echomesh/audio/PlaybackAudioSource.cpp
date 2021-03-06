#include "echomesh/audio/PlaybackAudioSource.h"

namespace echomesh {

void PlaybackAudioSource::prepareToPlay(int samplesPerBlockExpected,
                                        double /*sampleRate*/) {
  if (buffer_)
    buffer_->setSize(2, samplesPerBlockExpected, false, false, true);
  else
    buffer_ = new AudioSampleBuffer(2, samplesPerBlockExpected);

  info_.numSamples = samplesPerBlockExpected;
  info_.buffer = buffer_;
}

void PlaybackAudioSource::getNextAudioBlock(const AudioSourceChannelInfo& block) {
  ScopedLock l(lock_);

  if (not sources_.size()) {
    block.clearActiveBufferRegion();
    return;
  }
  sources_[0]->getNextAudioBlock(block);
  if (sources_.size() == 1)
    return;

  prepareToPlay(block.numSamples, 44100.0);
  for (int i = 1; i < sources_.size(); ++i) {
    sources_[i]->getNextAudioBlock(info_);
    for (int ch = 0; ch < 2; ++ch)
      block.buffer->addFrom(ch, 0, *info_.buffer, 0, 0, block.numSamples);
  }
}

void PlaybackAudioSource::addSource(AudioSource* source) {
  ScopedLock l(lock_);
  sources_.add(source);
}

void PlaybackAudioSource::removeSource(AudioSource* source) {
  ScopedLock l(lock_);
  sources_.removeObject(source);
}

}  // namespace echomesh
