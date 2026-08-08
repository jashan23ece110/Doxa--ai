// Logo animation states for Framer Motion

// Easing for smooth organic movement
const springTransition = {
  type: "spring",
  stiffness: 70,
  damping: 15,
  mass: 1
};

const organicTransition = {
  duration: 1.5,
  ease: [0.25, 0.1, 0.25, 1],
};

const fastTransition = {
  duration: 0.8,
  ease: "easeInOut"
};

export const logoVariants = {
  outer: {
    form: {
      scale: 1,
      y: 0,
      opacity: 1,
      rotate: 0,
      strokeDasharray: "300",
      strokeDashoffset: "0",
      transition: springTransition
    },
    deform: {
      scale: 1.1,
      y: -10,
      opacity: 0.8,
      rotate: 15,
      strokeDasharray: "150 50",
      strokeDashoffset: "-20",
      transition: organicTransition
    },
    transform: {
      scale: 1.25,
      y: -15,
      opacity: 0.6,
      rotate: 45,
      strokeDasharray: "80 40 40",
      strokeDashoffset: "-60",
      transition: organicTransition
    },
    reform: {
      scale: 1.05,
      y: -5,
      opacity: 0.9,
      rotate: 10,
      strokeDasharray: "200 20",
      strokeDashoffset: "-10",
      transition: organicTransition
    },
    finalForm: {
      scale: 1,
      y: 0,
      opacity: 1,
      rotate: 0,
      strokeDasharray: "300",
      strokeDashoffset: "0",
      transition: springTransition
    },
    reduced: {
      scale: 1, y: 0, opacity: 1, rotate: 0
    }
  },
  middle: {
    form: {
      scale: 1,
      y: 0,
      opacity: 1,
      rotate: 0,
      strokeDasharray: "200",
      strokeDashoffset: "0",
      transition: springTransition
    },
    deform: {
      scale: 0.9,
      y: 5,
      opacity: 0.9,
      rotate: -20,
      strokeDasharray: "100 30",
      strokeDashoffset: "20",
      transition: organicTransition
    },
    transform: {
      scale: 0.7,
      y: 10,
      opacity: 0.7,
      rotate: -90,
      strokeDasharray: "60 20",
      strokeDashoffset: "60",
      transition: organicTransition
    },
    reform: {
      scale: 0.95,
      y: 2,
      opacity: 0.9,
      rotate: -10,
      strokeDasharray: "150 10",
      strokeDashoffset: "10",
      transition: organicTransition
    },
    finalForm: {
      scale: 1,
      y: 0,
      opacity: 1,
      rotate: 0,
      strokeDasharray: "200",
      strokeDashoffset: "0",
      transition: springTransition
    },
    reduced: {
      scale: 1, y: 0, opacity: 1, rotate: 0
    }
  },
  inner: {
    form: {
      scale: 1,
      y: 0,
      opacity: 1,
      rotate: 0,
      strokeDasharray: "100",
      strokeDashoffset: "0",
      transition: springTransition
    },
    deform: {
      scale: 1.2,
      y: 15,
      opacity: 1,
      rotate: 45,
      strokeDasharray: "40 10",
      strokeDashoffset: "10",
      transition: organicTransition
    },
    transform: {
      scale: 1.5,
      y: 20,
      opacity: 1,
      rotate: 180,
      strokeDasharray: "20 5",
      strokeDashoffset: "30",
      transition: organicTransition
    },
    reform: {
      scale: 1.1,
      y: 5,
      opacity: 1,
      rotate: 20,
      strokeDasharray: "80 5",
      strokeDashoffset: "5",
      transition: organicTransition
    },
    finalForm: {
      scale: 1,
      y: 0,
      opacity: 1,
      rotate: 0,
      strokeDasharray: "100",
      strokeDashoffset: "0",
      transition: springTransition
    },
    reduced: {
      scale: 1, y: 0, opacity: 1, rotate: 0
    }
  }
};
