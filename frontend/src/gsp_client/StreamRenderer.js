class StreamRenderer {
  constructor(canvas_id) {
    this.canvas = document.getElementById(canvas_id);
    this.ctx = this.canvas.getContext("2d");

    this.isImageLoading = false;

    this.frame = new Image();
  }

  main_loop = () => {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.fillStyle = "#000000";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.fill();
    this.ctx.drawImage(this.frame, 0, 0, this.canvas.width, this.canvas.height);

    window.requestAnimationFrame(() => this.main_loop());
  };

  loadFrame = frameData => {
    if (this.isImageLoading) return;

    let image = new Image();
    image.src = frameData;

    this.isImageLoading = true;

    image.onload = evt => {
      this.frame = image;
      this.isImageLoading = false;
    };

    image.onerror = evt => {
      this.isImageLoading = false;
    };
  };

  start = () => {
    window.requestAnimationFrame(() => this.main_loop());
  };
}

export default StreamRenderer;
